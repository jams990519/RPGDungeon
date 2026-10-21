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
   | ✚ Curación | Utilidad de grupo (curas), Supervivencia | Daño sostenido, Ráfaga, Autonomía |
   | ✦ Soporte | Utilidad de grupo (potenciar y debilitar), Control | Ráfaga |

3. **Kit mínimo garantizado.** Toda spec tiene en su repertorio una interrupción (o algo equivalente), un defensivo mayor, un defensivo menor o autocuración, un control, una forma de reposicionarse o escapar, y un aporte de grupo. En WoW hubo clases que pasaron expansiones enteras sin interrupción o sin defensivos. Con la barra de 6 (D-46) no todo cabe a la vez: elegir qué llevar es parte del juego, pero toda spec tiene en su repertorio al menos una habilidad que **responde a los avisos** (bloquear, esquivar, escudo, cambiar de fila), y la configuración inicial de cada spec la trae puesta.

4. **Autonomía por rol (D-50).** Toda spec puede hacer sola el contenido en solitario (misiones, encargos, Profundidades normales). Lo que cambia es **cuánto tarda**, medido contra la mediana de las specs de Ataque en los mismos escenarios:

   | Rol | Tiempo para terminar (objetivo) | Margen aceptado | Cómo se sostiene solo |
   |---|---|---|---|
   | ⚔ Ataque | 1× (la referencia) | 0,9× a 1,1× | Mata rápido; se cubre con su respuesta al aviso y el cinturón |
   | ✦ Soporte | ~1,25× (algo más lento) | 1,15× a 1,35× | Sus potenciaciones también cuentan para él y su compañero |
   | 🛡 Defensa | ~1,5× | 1,4× a 1,6× | Casi no cae; el modo en solitario devuelve parte de lo que bloquea como daño |
   | ✚ Curación | ~2× (el doble) | 1,8× a 2,2× | Se cura a sí mismo; el modo en solitario pasa parte de la curación a daño |

   - **Siempre posible:** con juego básico (las Tácticas por defecto), toda spec gana al menos el 90 % de las peleas del contenido en solitario de su anillo. Un rol puede tardar más; nunca puede quedarse atascado.
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

8. **Mismo escalado con el equipo.** Todas las specs escalan igual con el Poder de Objeto. El simulador lo comprueba en cada anillo: ninguna spec puede "despertar" en el anillo VIII ni morirse en el III.

9. **Dificultad declarada, techo parejo.** Cada spec lleva una etiqueta de dificultad (★ a ★★★), y el simulador mide dos cosas:
   - **Juego básico**, con las [Tácticas](../04-combate/avisos-y-tacticas.md) automáticas por defecto: todas las specs a ±10 % de la mediana de su rol.
   - **Juego óptimo**, con el mejor plan posible: todas a ±3 % de la mediana de su rol.

   Así una spec fácil no domina y una difícil no queda inútil. En un juego por turnos no hay velocidad de dedos: la dificultad es **planificar**.

10. **Sin poder racial, sin poder prestado, sin clase obligatoria.** Los jefes se diseñan para composiciones libres; ninguna pelea pide "dos Chamanes".

## 3. Cómo se mide

**Simulador de combate** (el equivalente a SimulationCraft, módulo M21). Corre cada spec contra un conjunto fijo de escenarios en cada anillo de equipo (T1 a T10): un objetivo, varios objetivos, pelea con cambios de fila, pelea con fases, y PvP 1v1 contra cada una de las otras specs. Además corre:
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
| Victorias en solitario (juego básico) | Todas | 90 % o más en el contenido en solitario de su anillo |
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
- Mitigación de armadura con la fórmula **`def / (def + K)`** (la misma que usa TowerWars, con K = 60), con una K que crece por anillo para que la armadura nunca se convierta en inmunidad.
- Cada anillo sube los números alrededor de un 25 %, no un 100 %. Así el equipo de dos anillos atrás sigue sirviendo para algo: venderlo, desmontarlo o vestir a un alt.

## 5. La diferencia la hacen los oficios y el conocimiento

Si todas las clases rinden lo mismo, ¿qué separa a un jugador bueno de uno nuevo? Lo que **sabe** y lo que **sabe hacer**:

| Fuente de ventaja | Cómo ayuda en combate y en el mundo | Tope para que no se desboque |
|---|---|---|
| **Conocimiento del bestiario** | Ver la pista de los avisos, las debilidades y las partes rompibles de cada monstruo y jefe (ver [Avisos](../04-combate/avisos-y-tacticas.md)) | La pista ayuda a decidir, no decide por ti |
| **Oficios propios** | Fabricarte o mandarte a hacer mejor equipo; pociones, remedios y comidas de más calidad; curarte heridas tú mismo con Medicina | El equipo tiene techo por anillo; la toxicidad limita las pociones |
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

## 7. Registro de balance

### Octubre de 2026: especializaciones débiles al inicio y frente al Guardián

**Por qué.** Con el kit real (equipo inicial, pasiva de ~1 % por punto, barra automática), varias especializaciones perdían demasiado al nivel 2-3, sobre todo contra el Oso de las cumbres (Cazador · Puntería ganaba el 38 %), y frente al Guardián (Raigambre, nivel 6) el resultado iba del 0 % al 100 % según la especialización: las de soporte sin golpe temprano casi nunca ganaban y las de curación (y Paladín Protección) no perdían nunca.

**Objetivo de este ajuste** (pedido de la sesión de balance; no es una decisión del dueño): con juego básico, al nivel mínimo de cada enemigo de nivel 1 a 3, todas ganan el 90 % o más (curación, el 85 %); contra el Guardián al nivel 6, todas entre el 45 % y el 90 %; y ninguna barra queda muy por encima de su rol (`--bars --level=25`, +12).

**Cómo se midió** (todo con `tools/sim.py`):
- Enemigos tempranos: `--summary --real` (40 peleas por enemigo; números de abajo). Se confirmó con 80 a 100 peleas y otras semillas.
- Guardián: `--boss` (nuevo): nivel 6 con sus 5 puntos en la especialización, juego atento (lee el aviso, bloquea o esquiva, interrumpe, se cura, usa poción y venda), cinturón lleno (3 🧪 y 2 🩹) y, en las 7 ranuras, la mejor pieza normal de su tipo hasta **nivel de pieza 2 (poco común)**, que es lo que suele tener un héroe al nivel 6. 100 peleas por especialización; se confirmó con 300 y otras semillas.
- Ojo: el resultado contra el Guardián depende mucho del equipo. Con estos mismos números, con equipo de nivel 1 en todas las ranuras se gana el 17 % de media, y con piezas raras (nivel 3) en todas, el 98 %.
- La medición vieja de [Jefes](../06-contenido/jefes.md) §6 daba a cada héroe el doble de puntos de talento (un error del simulador de entonces) y solo 3 ranuras de equipo; por eso sus porcentajes no se comparan con estos.

**Enemigos.** Oso de las cumbres (`content/enemies.yaml`): vida base 120 → 110 y *Aplastar* 2,3 → 2,0. Era un pico injusto al nivel 3 para todas las clases que esquivan (su golpe grande no se esquiva). El Guardián no cambió.

**Especializaciones** (`content/classes.yaml`). Criterio: subir la **vida base** (y a veces el ataque base) de las débiles, porque pesa mucho al inicio y poco más tarde (al nivel 25, +30 de vida base es menos del 8 %); bajar la curación sostenida de las de curación (su segunda habilidad, que llega al nivel 4, y su recurso por ronda) y la segunda habilidad de las que ganaban siempre. "Peor % temprano" es la peor victoria contra un enemigo de nivel 1 a 3; "Guardián" es el % de victorias al nivel 6.

| Especialización | Peor % temprano | Guardián nivel 6 | Cambios |
|---|---|---|---|
| guerrero_furia | 90 → 100 | 9 → 60 | vida base 125 → 165; ataque base 13 → 15; defensa base 0.2 → 0.25; `golpe_colosal` valor 0.4 → 0.6 |
| guerrero | 100 → 100 | 27 → 68 | vida base 135 → 161 |
| guerrero_senor_guerra | 95 → 100 | 0 → 67 | vida base 130 → 169; ataque base 13 → 16; golpe básico 1.0 → 1.2; `estandarte_de_muralla` valor 0.35 → 0.5 |
| paladin_reprension | 100 → 100 | 45 → 64 | vida base 125 → 139 |
| paladin_proteccion | 100 → 100 | 100 → 81 | vida base 135 → 112; defensa base 0.22 → 0.17; `escudo_del_vengador` enfriamiento 3 → 5 |
| paladin_sagrado | 100 → 100 | 100 → 77 | vida base 115 → 105; defensa base 0.18 → 0.14; recurso por ronda 4 → 2; `destello_de_luz` valor 0.3 → 0.22; `faro_de_luz` valor 0.08 → 0.05 |
| cazador_punteria | 38 → 98 | 20 → 64 | vida base 110 → 122; `apuntar` rondas 2 → 3 |
| cazador_bestias | 100 → 100 | 77 → 77 | — |
| cazador_supervivencia | 100 → 100 | 4 → 61 | vida base 115 → 150 |
| picaro | 100 → 100 | 25 → 68 | vida base 105 → 134 |
| picaro_sutileza | 65 → 98 | 75 → 74 | vida base 105 → 110; `contraataque` potencia 1.7 → 1.6 |
| picaro_forajido | 85 → 100 | 16 → 59 | vida base 110 → 143 |
| sacerdote_sombra | 100 → 100 | 28 → 68 | vida base 100 → 122 |
| sacerdote_sagrado | 100 → 100 | 100 → 66 | `plegaria_de_sanacion` valor 0.32 → 0.28; `renovar` valor 0.08 → 0.05 |
| sacerdote | 100 → 100 | 97 → 64 | `escudo_de_luz` valor 0.3 → 0.23 |
| caballero_muerte_escarcha | 100 → 100 | 91 → 84 | `helada_mental` enfriamiento 3 → 5 |
| caballero_muerte_sangre | 100 → 100 | 54 → 54 | — |
| caballero_muerte_profano | 100 → 100 | 25 → 58 | vida base 125 → 162 |
| chaman_elemental | 100 → 100 | 79 → 79 | — |
| chaman_restauracion | 100 → 100 | 100 → 74 | recurso por ronda 4 → 3; `sanacion_en_cadena` valor 0.32 → 0.26; `totem_de_marea` valor 0.08 → 0.05 |
| chaman_totems | 90 → 100 | 6 → 74 | vida base 115 → 150; ataque base 12 → 13 |
| mago_fuego | 100 → 100 | 15 → 63 | vida base 100 → 130 |
| mago_escarcha | 90 → 100 | 20 → 67 | vida base 100 → 121 |
| mago_arcano | 100 → 100 | 0 → 67 | vida base 110 → 143; ataque base 13 → 16 |
| brujo_destruccion | 100 → 100 | 92 → 81 | `inmolar` potencia 0.6 → 0.5 |
| brujo_demonologia | 100 → 100 | 29 → 74 | vida base 120 → 144 |
| brujo_afliccion | 100 → 100 | 46 → 65 | vida base 110 → 124 |
| monje_viajero_viento | 100 → 100 | 28 → 70 | vida base 110 → 137 |
| monje_maestro_cervecero | 100 → 100 | 75 → 75 | — |
| monje_tejedor_niebla | 72 → 90 | 100 → 78 | vida base 105 → 112; `niebla_envolvente` valor 0.08 → 0.07; `vivificar` valor 0.3 → 0.2 |
| druida_feral | 100 → 100 | 99 → 76 | `desgarrar` potencia 0.6 → 0.4 |
| druida_guardian | 100 → 100 | 89 → 77 | `pelaje_de_hierro` valor 0.7 → 0.65 |
| druida_restauracion | 100 → 100 | 100 → 73 | `rejuvenecimiento` valor 0.08 → 0.06; `alivio_presto` valor 0.3 → 0.2 |
| cazador_demonios_estrago | 100 → 100 | 31 → 70 | vida base 120 → 137 |
| cazador_demonios_venganza | 100 → 100 | 89 → 76 | `puas_demoniacas` valor 0.7 → 0.6 |
| cazador_demonios_devorador | 92 → 100 | 2 → 61 | vida base 120 → 156; ataque base 12 → 15 |
| evocador_devastacion | 100 → 100 | 83 → 83 | — |
| evocador_preservacion | 85 → 90 | 100 → 72 | recurso por ronda 10 → 6; `eco` valor 0.08 → 0.06; `rebobinar` valor 0.32 → 0.21 |
| evocador_aumentacion | 92 → 100 | 0 → 65 | vida base 115 → 150; ataque base 12 → 15; `presciencia` valor 0.5 → 0.7 |
| nigromante_plaga | 98 → 100 | 53 → 67 | vida base 105 → 110 |
| nigromante_legion | 98 → 100 | 89 → 78 | `levantar_esqueletos` potencia 0.7 → 0.6 |
| nigromante_drenaje | 78 → 100 | 24 → 70 | vida base 100 → 118 |
| bardo_duelista | 100 → 100 | 65 → 65 | — |
| bardo_trovador | 82 → 90 | 100 → 62 | vida base 105 → 107; recurso por ronda 10 → 6; `balada_curativa` valor 0.08 → 0.06; `nota_curativa` valor 0.3 → 0.2 |
| bardo_estratega | 78 → 100 | 1 → 61 | vida base 110 → 143; ataque base 12 → 15 |

**Resultado.** Tempranos: la peor es 90 % (Monje Tejedor de niebla, Evocador Preservación y Bardo Trovador, de curación, contra el Oso de las cumbres); las demás, 98 % o más. Guardián: entre 54 % (Caballero de la Muerte Sangre) y 84 % (Caballero de la Muerte Escarcha), media de 70 %. Barras al nivel 11 y al 25: ninguna queda más de 12 puntos por encima de su rol; la mediana de vida restante de Curación baja de 83 % a 79 % (seguía siendo el rol más alto) y las demás quedan entre 68 % y 70 %.

**Lo que queda por mirar:** el Guardián premia mucho las respuestas de escudo y de esquiva (el escudo frena cualquier golpe y casi todos sus golpes grandes de la última fase se esquivan o se interrumpen), y castiga la falta de golpe en la barra. Eso se nota en la forma de los números, no en los porcentajes de hoy; si se agregan más jefes, conviene medir cada uno con `--boss`.

### Octubre de 2026: la despensa del asentamiento (D-93, provisional)

**Por qué.** El dueño aceptó por voz que subir de etapa pida algo más que pagar materiales. Primera parte: la despensa (ver [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §0.4). Son números **nuevos**, no movidos: salen de las tablas de esa propuesta (§3.2, §4.2, §7) y todavía no se midieron con jugadores. Se ajustan en la beta.

**Números nuevos** (`content/balance.yaml` → `pantry`, `content/items.yaml`, `content/enemies.yaml`):

| Número | Valor | De dónde sale |
|---|---|---|
| Despensa del Claro | ~~desde aldea~~ **nunca** (D-95, 0.10.1) | El Claro no tiene dueño: no se mantiene |
| Despensa de los campamentos desde | nivel 3 | §7.2, capa ligera |
| Consumo | 1 ración por residente activo por día real | §4.2 |
| Activo | tocó un botón en las últimas 24 h (marca renovada cada 60 min) | §2.1 y §15.3: quien no juega no come |
| Despensa nueva | 7 días para todos los miembros del campamento | §15: nadie empieza castigado |
| Estados (días) | abundancia 14 · holgada 7 · justa 3 · escasez 1 · hambruna 0 | §3.2 |
| ~~Días para subir el Claro~~ | ~~pueblo 4 · ciudad 5 · castillo 7~~ | Quitados en la 0.10.1 (D-95) |
| Experiencia y mérito por ración | 2 y 1 | Como un material de la obra común (`settlement.xp_per_unit`) |
| 🍖 Carne | 2 raciones; 40-60 % por victoria contra bestias; 1-2 piezas; se vende a 1 🥉 | §4.1 (caza), en chico |
| 🥖 Provisiones | 1 ración; 15 🥉 en el mercader; no se revenden | §15.8: comida de emergencia cara |

**Cuenta rápida.** Una victoria contra un lobo deja en promedio 0,5 × 1,5 × 2 = 1,5 raciones. Con 40 de energía por día, quien pelea seguido gana muchas más raciones de las que come (1 por día): la comida no falta si los que pelean la llevan a la despensa. Lo que se pone a prueba es la **participación**, no la producción. Alimentarse solo con provisiones cuesta 15 🥉 por persona y día (unas tres peleas tempranas de monedas).

**Lo que queda por mirar:** si la carne alcanza de sobra (bajar la probabilidad o el valor), el tope por semana de las provisiones (§15.8) y si hace falta un tope de capacidad antes de los graneros (§4.3). Medir en la beta cuántos días alcanza la despensa de un campamento con sus miembros reales.

### Octubre de 2026: mochila llena y cofre (D-90 y D-92, provisionales)

**Por qué.** El dueño aceptó por voz dos reglas. **Mochila llena (D-90):** lo que encuentras nunca se pierde, pero con la mochila llena no se recolecta ni se compra hasta vender o usar cosas. **Cofre (D-92, resuelve P-73):** el 🪎 cofre entra como moneda que se arma con bolsas y paga lo grande; el 💵 billete no entra. Son números **nuevos**, no movidos: los propuso Claude y todavía no se midieron con jugadores.

**Lo que no cambia:** el espacio de la mochila sigue en 60 (`hero.backpack_capacity`). Cambia la regla: antes los hallazgos de explorar se perdían con la mochila llena y comprar no miraba el espacio; ahora los hallazgos entran siempre y comprar espera, como recolectar.

**Números nuevos** (`content/balance.yaml`):

| Número | Valor | De dónde sale |
|---|---|---|
| Receta del cofre (`currency.chest_recipe`) | 10 💰 bolsas + 10 de madera + 5 piezas de metal | P-73: "se arma con 10 bolsas, madera y metal" |
| Agrandar con cofres desde (`camps.chests_from_level`) | nivel 6 (el paso de 6 a 7, hacia ciudad) | P-73: "paga lo grande (campamentos altos, castillos)" |
| Cofres por nivel (`camps.chests_per_level`) | 1 × (nivel actual − 6 + 1): 1 de 6 a 7, 2 de 7 a 8, 3 de 8 a 9, y sigue subiendo de a 1 | Pedido del dueño: 1 + (nivel − 6) |
| Icono (`currency.icons.chests`) | 🪎 | D-85: el icono que mostró el dueño |

**Cuenta rápida.** Un cofre resume 10 bolsas (40 de fibra, 10 de metal y 10 🥈) más 10 de madera y 5 de metal: **40 de fibra, 15 de metal, 10 de madera y 10 🥈**. De nivel 6 a castillo (9) hacen falta 6 cofres: 240 de fibra, 90 de metal, 60 de madera y 60 🥈, además de los materiales de siempre (90 + 105 + 120 de madera, etc.). Los materiales de un cofre (65 unidades) caben en uno o dos días de energía de un jugador; lo que más pesa son las 10 🥈 (1.000 🥉), porque una pelea temprana deja unos 5 🥉. Entre los miembros de un campamento de nivel 6 (hasta 12 personas) se reparte rápido. Es el sumidero más grande del juego hoy, a propósito: frena a los campamentos grandes y saca plata del juego.

**Lo que queda por mirar:** si los campamentos de nivel 6 se quedan trabados (bajar la receta o subir `chests_from_level`), si conviene que los miembros junten cofres entre todos (un almacén común, ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md)) y si la mochila llena empuja a vender demasiado (más bronce entra al juego) o a aportar a la obra y a la despensa de los campamentos. Medir en la beta.

### Octubre de 2026: jugadores en la zona (D-96, provisional)

**Por qué.** El dueño pidió por voz ver, al tocar 📍 Zona, a los otros jugadores que están en tu zona y lo que hacen, y toparte con ellos al explorar (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.13). Son números **nuevos** (`content/balance.yaml` → `presence`), propuestos por Claude. No tocan el combate, la economía ni la experiencia: solo deciden qué se muestra.

| Número | Valor | Por qué |
|---|---|---|
| Presente si tocó un botón hace menos de | 15 minutos | Lo bastante corto para que la lista sea "quién está ahora"; quien explora, recolecta o duerme ahí cuenta aunque no toque botones |
| Nombres en 📍 Zona | 5, y "… y N más" | Pantallas cortas (D-86): el bloque suma como mucho 7 líneas |
| Cruce por vuelta de exploración o recolección | 15 % | Con alguien presente todo el lote, 10 vueltas dan en promedio 1,5 sorteos ganados; como a cada jugador te lo cruzas una sola vez por lote, el resumen suma pocas líneas |

**Lo que queda por mirar:** en la beta, si el Claro se llena (más de 5 presentes seguido) y conviene mostrar primero a los que hacen algo, o subir el tope.

### Octubre de 2026: el gremio del campamento (D-97, provisional)

**Por qué.** El dueño pidió por voz que, desde tu campamento, se pueda crear un gremio que deje entrar a más gente a medida que progresa, con requisitos de exploraciones, combates y misiones, y que sirva para tener un castillo (ver [Gremios y vida social](../08-social/gremios-y-social.md) §0). Son números **nuevos**, no movidos, propuestos por Claude. Todavía no se midieron con jugadores: se ajustan en la beta.

**Números nuevos** (`content/balance.yaml` → `guild`):

| Número | Valor | Por qué |
|---|---|---|
| Crear el gremio | 50 🥉 | Un sumidero chico: crear el campamento ya costó progreso |
| Cupo por nivel (1 a 8) | 4 · 6 · 8 · 12 · 16 · 20 · 25 · 30 | Con gremio, reemplaza a la cuenta de antes (2 + 2 por nivel del campamento); nadie sale si baja |
| Subir del nivel 1 al 2 | 40 exploraciones, 20 peleas ganadas y 100 recursos | Un grupo chico lo logra en uno o dos días: el primer paso se siente rápido |
| Cada nivel siguiente | ~×1,6 (hasta 670, 335 y 1.680 para el 7 → 8) | Como la obra del Claro: cada etapa pide bastante más |
| Castillo | Gremio de nivel 5 o más y 10 miembros o más | El castillo es de un grupo, no de una persona sola |

**Cuenta rápida.** Cada exploración y cada recolección gastan 1 de energía (40 por día). Un miembro que reparte su energía entre explorar y recolectar suma por día unas 20 exploraciones, 6 a 8 peleas ganadas y 50 a 60 recursos (con el 50 % extra de su territorio). Llegar al nivel 5 pide en total 370 exploraciones, 182 victorias y 930 recursos: un grupo activo de 4 a 6 miembros lo logra en una semana. Lo que más frena al castillo es juntar 10 miembros, no los contadores, y eso es a propósito.

**Lo que queda por mirar:** si las victorias frenan más que lo demás (en el territorio no hay peleas), si conviene que la comida aportada a la despensa cuente, y qué pedirán las misiones cuando existan. Medir en la beta cuántos días tarda un gremio real en cada nivel.

### Octubre de 2026: vida en 4 horas y experiencia por explorar (D-103 y D-104)

**Por qué.** El dueño pidió que la vida vuelva cada 4 horas y que explorar dé experiencia.

| Número | Antes | Ahora | Qué mueve |
|---|---|---|---|
| Vida de 0 a llena fuera de combate (`regen.hp_full_minutes`) | 100 min (1 % por minuto) | **240 min** | Las pociones y la posada pesan más; entre peleas hay que esperar o curarse. El combate no cambia |
| Vida si caíste (`regen.downed_full_minutes`) | 500 min (0,2 % por minuto) | 500 min (mismo número, otra forma de escribirlo) | Sigue siendo mucho más lento que lo normal (D-83) |
| Experiencia por vuelta de exploración (`explore.xp_per_step`) | 0 | **3** | Con 40 de energía al día, explorar da hasta 120 de experiencia diaria más los extras de zona: menos que pelear, pero sin riesgo |
| Extra al dejar una zona al 100 % (`explore.xp_full_zone`) | 0 | **15** | Premia terminar zonas (unas 4-6 vueltas cada una) |
| Casillas de alrededor que se exploran sin moverte (`explore.around_radius`) | 0 (solo tu zona) | **1** (las 8 vecinas), desde 0.13.1 (D-107) | Un lote grande ya no se corta al 100 %: sigue con las vecinas. Más experiencia por explorar en el mismo lugar (cada vecina da sus 15 al completarla) y más zonas conocidas para fundar campamento |

### Octubre de 2026: cada camino llega al nivel 100 (D-108)

**Por qué.** El dueño pidió que cada forma de jugar (recolectar, cazar, pelear, explorar) alcance por sí sola para llegar al nivel 100, sin aburrir. Antes, recolectar no daba experiencia directa: solo recolectando, el nivel 100 llegaba en unos 6,5 años, contra 1,9 explorando.

| Número | Antes | Ahora | Qué mueve |
|---|---|---|---|
| Experiencia por recolección (`gather.xp_per_step`) | 0 | **14** × (1 + 0,15 × (nivel de la zona − 1)), solo si juntaste algo | Solo recolectando, el nivel 100 llega en ~2 años (con toda la energía y peleas ganadas); en tu territorio, sin peleas, ~2,9 |
| Escala por nivel (`hero.xp_level_scale`) | 0,15 escrito en el código del combate | **0,15** en balance.yaml (mismo número) | Ahora lo comparten matar y recolectar: moverlo cambia el ritmo de todos los caminos a la vez |
| Energía por presa al cazar (`hunt.energy`, D-106) | — | **2 ⚡** (en el juego con la cacería) | Con 1 ⚡ por presa, cazar llevaría al 100 en 0,9 años: el doble de rápido que lo demás |

**Lo que queda por mirar:** el ritmo real con viajes y derrotas (medir en la beta) y si recolectar en el territorio propio, sin riesgo, rinde demasiado.

**Lo que queda por mirar:** si explorar compite demasiado con pelear para subir de nivel (la meta de 100 niveles en 2-3 años, D-78).

### Octubre de 2026: el bestiario por niveles (D-108)

**Por qué.** El dueño pidió que cada camino llegue al nivel 100 sin aburrir (D-108, confirmada). Antes casi todos los enemigos llegaban hasta el nivel 16: más arriba, pelear y cazar era el bandido errante una y otra vez. Se sumaron **87 enemigos** en `content/enemies.yaml` (sección D-108, al final del archivo), con sus textos en `content/locales/es.yaml`. Son números **nuevos**: ningún enemigo que ya estaba cambió, ni `balance.yaml`. La lista por bioma está en [Bestiario](../06-contenido/bestiario.md), «En el juego».

**Números nuevos:**

| Número | Valor | Por qué |
|---|---|---|
| Franjas | 1-15, 12-30, 25-45, 40-60, 55-75, 70-90, 85-100, que se pisan | Cada bioma con peligro tiene al menos 2 enemigos propios en cada nivel del 2 al 100, sin contar al bandido (`tests/test_bestiary.py`) |
| Curva de base | vida 75 + 13 por nivel; ataque 10 + 1,5 por nivel | La del bandido errante, que ya escalaba parejo del 3 al 99: con equipo poco común deja el 67-75 % de la vida a cualquier nivel |
| Moldes (vida × ataque, defensa, iniciativa) | fiera 1,35 × 1,2, 5 %, 13 · bruto 1,42 × 1,05, 20 %, 6 · coraza 1,22 × 1,0, 38 %, 5 · veneno 1,05 × 1,18, 12 %, 12 · espectro 1,13 × 1,32, 0 %, 11 · soldado 1,35 × 1,1, 20 %, 9 · enjambre 0,95 × 1,2, 0 %, 15 | Ajustados con el simulador para que cada molde deje entre el 52 % y el 67 % de la vida: se gana casi siempre, pero cuesta |
| Franja (multiplica vida y ataque) | 0,85 (zonas bajas de montaña, tundra, desierto y ruinas) · 0,95 (niveles 6-17) · 1,0 · 1,02 · 1,04 · 1,05 · 1,06 · 1,08 (franjas 2 a 7) | El mundo se pone un poco más duro a medida que te alejas, sin cambiar el ritmo |
| Experiencia de base | 34 · 40 · 42 · 42 · 43 · 43 · 44 · 44 según la franja, × molde (bruto 1,12, coraza 1,08, soldado 1,05, fiera 1,0, veneno y espectro 0,97, enjambre 0,9) | Crece poco con la franja para que el ritmo de D-108 no cambie (cuenta abajo) |
| Monedas | de 2-6 (franja 1) a 6-14 (franja 7); las bestias, 1-2 menos; la gente y los gigantes, 2-3 más | Como antes, `gold` se multiplica por 1 + 0,1 × (nivel − 1) |
| Botín | material principal del 20 % (franja 1) al 50 % (franja 7), el segundo 12 puntos menos; pociones o vendas del 9 % al 19 % en la gente y los espectros; 🍖 carne 40-60 % en las bestias que se comen (D-93) | El botín crece con la franja |
| Golpes | sin mecánicas nuevas; desde la franja 5, 3 golpes o más: brutos, venenosos y enjambres suman un segundo golpe grande (1,7 a 1,8); los demás, una carga | Variedad: hay que leer el aviso para elegir la respuesta |

**Cómo se midió.** Con las funciones de `tools/sim.py` (las del modo `--boss`): cada enemigo nuevo a su nivel mínimo, medio y máximo, contra un héroe del mismo nivel con sus nivel − 1 puntos en la especialización (barra automática y pasivas), juego atento, cinturón lleno (3 🧪 y 2 🩹) y, en las 7 ranuras, la mejor pieza normal de su tipo hasta el nivel de pieza indicado. Las 45 especializaciones, 20 peleas por punto. La referencia es **equipo poco común (nivel de pieza 2)**, lo que tiene casi cualquier héroe después del nivel 3.

| Franja | Enemigos | Victorias (media) | Peor especialización | Vida que queda | Rondas |
|---|---|---|---|---|---|
| 1-15 (relleno) | 13 | 100 % | 95 % (Nigromante Plaga contra el Jabalí colmillo de hierro, nivel 17) | 55-76 % | 11,7 |
| 12-30 | 17 | 100 % | 95 % (Nigromante Plaga contra el Ogro del puente, nivel 21) | 52-62 % | 12,4 |
| 25-45 | 13 | 99,9 % | 85 % (Nigromante Plaga contra el Trol de las colinas, nivel 25) | 53-65 % | 12,9 |
| 40-60 | 11 | 99,9 % | 85 % (Bardo Duelista contra el Wyrm joven de las dunas, nivel 43) | 55-67 % | 10,9 |
| 55-75 | 11 | 99,9 % | 80 % (Druida Feral contra el Draco de escarcha, nivel 65) | 55-65 % | 12,2 |
| 70-90 | 11 | 99,8 % | 75 % (Mago Arcano contra la Abominación del cieno, nivel 90) | 54-66 % | 12,5 |
| 85-100 | 11 | 99,8 % | 80 % (Mago Arcano contra el Titán de las llanuras, nivel 100) | 54-64 % | 12,9 |

- Con el mismo juego, los enemigos de antes dejan: bandido errante 67-75 %, lobo ceniciento 87 %, oso de las cumbres y caimán de lodo 53 %. Los nuevos quedan entre el bandido y el oso.
- Con equipo raro (nivel de pieza 3): 100 % de media, la peor especialización 90 % o más, 56-80 % de vida.
- Con el equipo inicial (nivel de pieza 1): 98-100 % de media, pero las especializaciones con poca vida (Mago Arcano, Druida Feral, Bardo Duelista, Nigromante Plaga, Pícaro) ganan solo el 30-55 % contra los brutos de las franjas altas.
- `tools/sim.py --summary --real` (enemigos de nivel 1 a 3, juego básico) no cambia: la peor sigue siendo 90 % contra el Oso de las cumbres; los 7 enemigos nuevos de nivel bajo no bajan a nadie.

**El ritmo de D-108.** Con una pelea ganada cada 2 ⚡ (20 por día) en zonas de tu nivel, promediando los 8 biomas con peligro y el 30 % de enemigos con un nivel más, el nivel 100 llega en **1,81 años** (antes, con el bandido solo arriba del 16, en 1,80). Experiencia por pelea: al nivel 50, 376 (antes 378); al nivel 90, 654 (antes 648). `tests/test_bestiary.py` comprueba que el ritmo quede entre 1,7 y 2,1 años.

**0.28, terrenos nuevos (D-188).** Los 6 terrenos nuevos no traen enemigos nuevos: usan los de terrenos parecidos, con 2 o más en cada franja. Promediando los **14** terrenos con peligro, el ritmo queda en **1,82 años** (con los 8 de antes, 1,82 también); experiencia por pelea al nivel 50, 374 (igual); al 90, 651 (antes 652). Ningún número de balance se movió. `tests/test_bestiary.py` y `tests/test_terrenos_nuevos.py` lo comprueban.

**Qué enemigo sale (arreglo).** La regla de los encuentros pasó a `engine/world/encounters.py` y la usan también las incursiones. Antes, en una zona sin enemigo para su nivel salía cualquiera del bioma con su nivel tope (en una zona de nivel 120, un lobo de nivel 6). Ahora salen los de la franja más cercana.

**Efecto en las incursiones (D-99).** La Noche de prueba trae al más fuerte del bioma, y antes, arriba del nivel 16, ese era siempre el bandido: con equipo inicial se ganaba el 83-93 % de las veces. Ahora es un monstruo de la franja (un bruto casi siempre) y se gana el 37-57 % con equipo inicial y el 58-74 % con equipo poco común, al nivel de la zona: vuelve a parecerse a lo que pedía D-99 («cerca de la mitad»). En las zonas de nivel 10 se volvió más fácil (54 % contra 23 % antes), porque ya no trae al caimán o al oso cavernario sino otro de la misma franja. La incursión semanal sigue ganándose casi siempre.

**Lo que queda por mirar:**
- **Equipo de nivel alto:** ~~las piezas llegan solo hasta el nivel requerido 8~~ **hecho** en la pasada de D-110: piezas cada 10 niveles hasta el 100, y si la ventana de nivel cae entre dos, el botín usa la más cercana por debajo. Desde esa pasada los enemigos comunes son más fuertes desde el nivel 3 (vida por nivel × 1,3 y ataque por nivel × 1,8): los números de esta sección (vida que queda, "con equipo poco común deja el 67-75 %") son de antes.
- **Especializaciones con poca vida** a niveles altos con el equipo inicial (lista de arriba): **revisadas** en la pasada de D-110 (con el equipo de su nivel quedan cerca de la mediana de su rol).
- **La piel de los oficios (D-109):** cuando entren los oficios, sumar la piel a las bestias nuevas (las que sueltan 🍖 carne).
- `tools/sim.py --bars` y el modo sin opciones recorren ahora 104 enemigos: tardan más. Si molesta, filtrar por los enemigos que caben en el nivel medido.

### Octubre de 2026: las incursiones de los campamentos (D-99, provisional)

**Por qué.** Segunda parte de "construir no alcanza", después de la despensa: desde que se fundan (D-105; antes desde pueblo, nivel 5) los campamentos de jugadores reciben una incursión ("oleada") por semana, y pasar a castillo pide ganar la Noche de prueba (ver [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §0.5 y §7.2). El Claro nunca tiene incursiones: es el campamento base (D-95, D-98). Son números **nuevos**, no movidos, y se ajustan en la beta.

**Números nuevos** (`content/balance.yaml` → `raids`):

| Número | Valor | De dónde sale |
|---|---|---|
| Desde qué nivel | ~~5 (pueblo)~~ → **1: desde que se funda**, con aviso al fundarlo (movido el 1-oct-2026, D-105) | §7.2, capa ligera; el dueño las quiere desde la fundación |
| Cada cuánto | 7 días reales (reloj perezoso: llega cuando un miembro juega después de esa hora) | §7.2: "una incursión por semana" |
| Ventana del aviso | 60 minutos, más 15 de espera para una pelea que ya empezó | Que dé tiempo a los conectados sin trabar la semana |
| Victorias necesarias | la mitad de los miembros activos al llegar, hacia arriba; al menos 1 | §7.2: fuerza escalada a los miembros activos |
| Si se pierde | la despensa pierde el 25 % de sus raciones; nada más | §6.5 (entre la brecha parcial, 15 %, y la derrota, 30 %) y §15 |
| Enemigo | del bioma del campamento, nivel de la zona + 1 | §6.2: nunca más de + 2 |
| Premio por defender | 80 de experiencia y 30 🥉 a cada defensor, además del premio de su pelea | Chico: como una pelea más y dos 🥖 provisiones |
| Noche de prueba: victorias | la mitad de los activos, hacia arriba; al menos 2 | El castillo se gana en conjunto |
| Noche de prueba: enemigo | el más fuerte del bioma (vida × ataque), nivel de la zona + 2, con vida × 2 y ataque × 1,3 | §6.4 en chico: un jefe de la zona sin fases |
| Noche de prueba: si se pierde | nada; se reintenta a los 2 días | §7.1 y §7.2 |
| Noche de prueba: premio | 200 de experiencia y 100 🥉 (1 🥈) a cada defensor | Una vez por campamento |

**Cuenta rápida** (medida aparte con las funciones de `tools/sim.py`: la forma de jugar atenta, cinturón lleno, las 45 especializaciones activas, cada bioma). Contra el enemigo de la incursión semanal, un héroe del nivel de la zona gana casi siempre (99-100 %): la incursión pone a prueba la **participación**, no la fuerza, igual que la despensa. La Noche de prueba sí pesa: con el equipo inicial y el nivel de la zona gana cerca de la mitad de las veces (45-51 %, y muy poco contra el caimán del pantano o el oso cavernario de las colinas); con 3 a 5 niveles más y equipo poco común, entre el 86 % y el 100 %. Perder una incursión con 4 miembros activos y la despensa en 28 raciones cuesta 7 raciones: casi 2 días de comida.

**Lo que queda por mirar:** si la incursión semanal es demasiado fácil cuando los miembros superan mucho el nivel de su zona (subir `enemy_level_bonus` hasta 2, el tope de §6.2), si 60 minutos alcanzan para los husos horarios de los miembros (el Eco de §6.5 lo resolvería), y si el mínimo de 2 victorias de la Noche de prueba deja trabado a un campamento de una sola persona (hoy sí lo traba: castillo pide al menos dos miembros activos).

### Octubre de 2026: las mejoras del campamento (D-101, provisional)

**Por qué.** El dueño pidió por voz "más división": que para llegar a castillo hagan falta unas 15 mejoras del campamento o más, y que, como llegan oleadas desde la fundación (D-105), haya que "reforzar las cosas en los alrededores" (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §2.6). Son números **nuevos**, propuestos por Claude; ninguno se movió. Todavía no se midieron con jugadores.

**Números nuevos** (`content/camp_upgrades.yaml` y `content/balance.yaml` → `upgrades`):

| Número | Valor | Por qué |
|---|---|---|
| Mejoras en total | 20, de los niveles 1 a 8 (2, 2, 4, 3, 3, 2, 2, 2) | Cada etapa abre algo; con el nivel 8 se elige cuáles 15 hacer |
| Para castillo (`upgrades.castle_min_built`) | 15 construidas | Lo pidió el dueño ("unas 15 o más") |
| Costo de las de nivel 1 (Fogón, Empalizada) | 35 y 40 materiales | Dos jugadores las levantan en un día |
| Costo por nivel | ~70 (nivel 2), ~120 (3), ~200 (4), ~300 (5), ~330 (6), ~500 (7), ~580 (8) materiales | Sube como el costo de agrandar; la piedra pesa más en las defensas grandes |
| Monedas | Puesto de trueque 1 🥈, Taller 2 🥈, Herrería 3 🥈, Enfermería 3 🥈, Biblioteca 5 🥈 (14 🥈 en total) | Sumidero de monedas en los servicios, que ahorran viajes al Claro |
| Experiencia por material aportado (`upgrades.xp_per_unit`) | 1 (y 1 de mérito) | La mitad de lo que daba la obra del Claro (2): aportar no debe competir con pelear o explorar (D-78) |
| Fogón / Enfermería | vida ×1,5 / vida tras caer ×1,5, solo miembros en el territorio | Descansar en casa ayuda, sin reemplazar pociones ni la posada |
| Refugio | 2 🥉 y 5 minutos (la posada del Claro: 4 🥉) | Más barato por quedar lejos del mercader |
| Puesto de trueque | mitad de precio, como el mercader; la comida nunca | Ahorra el viaje; no cambia el precio |
| Granero / Ahumadero / Huerto | −10 % de consumo / +1 ración por carne / +1 ración por día | Ayudas chicas: la despensa sigue dependiendo de cazar |
| Pozo | recursos del territorio ×1,5 más rápido (`stock.regen_per_hour` 2 % → 3 % por hora) | Un territorio agotado vuelve en ~33 horas en vez de ~50 |
| Cabañas | +2 miembros de cupo | Ayuda a juntar los 10 del castillo |
| 🛡️ Defensa | 11 puntos con las 8 defensas (12 de noche con los Braseros) | Escala de 0 a 11 que leen las oleadas |
| Cuánto frena cada punto (`raids.defense_weaken_per_point`) | **4 %** menos de vida y de ataque a los atacantes; con 11 puntos, 44 % | Conectado en la 0.14: se nota desde la Empalizada sin volver trivial la pelea |
| Tope (`raids.defense_floor`) | los atacantes nunca bajan de la **mitad** | Defender sigue siendo pelear |
| Noche de los Braseros (`raids.night`) | de 19 a 6 h, hora UTC−5 | Provisional: el mundo todavía no tiene día y noche |
| Conocimiento | Herramientas +10 % al recolectar, Cartografía +5 puntos por vuelta, Rastreo +10 % de carne; 200 a 230 materiales y 3 🥈 cada uno | Modestos a propósito: el territorio ya da +50 % al recolectar (hasta la 0.48: D-309 lo cambió por la 🌾 cosecha de la muralla) |

**Cuenta rápida.** Un miembro que recolecta en su territorio junta unos 4 a 5 materiales por energía (con el +50 %); dedicando la mitad de su energía, unos 60 a 80 por día. Las 15 mejoras más baratas suman unos **2.500 materiales y 3 🥈**: un grupo de 5 que además agranda el campamento (unos 1.100 materiales y 6 🪎 cofres hasta castillo) tarda **varias semanas**, al ritmo del gremio de nivel 5 y de la Noche de prueba. Las 20 suman unos 5.000 materiales.

**Lo que queda por mirar:** cuánto tarda de verdad un grupo en las 15 (si se traba en la piedra de la Muralla y el Foso, bajar esos costos), si la Perrera y el Rastreo, que piden carne, dejan la despensa corta, y si el 4 % por punto de 🛡️ Defensa (conectado en la 0.14) deja las oleadas demasiado fáciles para un campamento con las 8 defensas.

### Octubre de 2026: la cacería en la zona y la partida de caza (D-106, provisional)

**Por qué.** El dueño pidió por voz un formato de cacería en la misma zona, para pelear solo contra monstruos, y que los miembros de un campamento puedan ir juntos a cazar (ver [Cacerías](../06-contenido/cacerias.md) §0). Son números **nuevos**, no movidos: los 2 ⚡ por presa los fijó D-108 (confirmada) y los de la partida los propuso Claude. Todavía no se midieron con jugadores: se ajustan en la beta.

**Números nuevos** (`content/balance.yaml` → `hunt`):

| Número | Valor | Por qué |
|---|---|---|
| Energía por presa (`hunt.energy`) | 2 | Lo fijó D-108 (confirmada): con 2, cazar da una experiencia por ⚡ parecida a explorar y recolectar; la pelea en sí no gasta (D-78) |
| Duración de la partida (`party.minutes`) | 30 minutos | Una sesión corta de Telegram; la mitad de la ventana de una oleada |
| Bono por compañero presente (`party.bonus_per_companion`) | +10 % de experiencia y de probabilidad de botín | Se nota sin obligar a jugar en grupo; nunca toca las monedas |
| Tope del bono (`party.bonus_cap`) | +30 % (3 compañeros) | Que un grupo grande no multiplique el ritmo de subida |
| Meta (`party.prey_per_hunter`, `min_hunters`) | 3 presas por cazador, contando al menos 2 | Crece con el grupo: lo mismo por cabeza en una partida de 2 o de 5 |
| Premio (`party.reward`) | 40 de experiencia y 20 🥉 a cada cazador con al menos 1 presa | Chico: como una presa más; la mitad del premio de una oleada |

**Cuenta rápida.** Explorar da por cada energía 3 de experiencia, más o menos media pelea y lo que se encuentra (D-104); cazar da una pelea entera cada 2 de energía: un lobo de nivel 1 vale 30 de experiencia, 15 por ⚡, casi lo mismo que explorar (~16). Es la cuenta de D-108: solo cazando, el nivel 100 llega en ~1,8 años, como los demás caminos (con 1 ⚡ por presa serían 0,9). Cazar no da exploración, objetos ni monedas sueltas, ni recursos, y gasta vida (vuelve en 4 horas, D-103) y pociones. El freno real es la vida, no la energía: tocando solo ⚔️ Atacar, un guerrero de nivel 1 pierde cerca de un tercio de su vida por presa al lado del Claro (medido con el motor en 40 mundos: gana 39 de 40), así que caza 2 o 3 presas seguidas antes de curarse. Con la partida al tope (+30 %), la experiencia de cada presa sube un 30 %: "un poco más rápido", como dice [Progresión](progresion.md) §1.2. Cada presa ganada cuenta también como victoria del gremio (D-97), así que los gremios que cazan juntan las victorias más rápido.

**Lo que queda por mirar:** si la partida de caza al tope acelera demasiado la subida de nivel (D-108 pide caminos parejos; si pasa, bajar `bonus_cap`), si las victorias de la cacería hacen demasiado fácil el contador de victorias del gremio, y si 30 minutos alcanzan para juntar a los miembros. Medir en la beta cuántas presas caza un jugador por día y cuántas partidas llegan a la meta.

### Octubre de 2026: corrida de diagnóstico de clases y roles (D-110)

**Qué se midió.** Las 45 especializaciones, con todos sus puntos en la especialización, jugando de forma básica contra todos los enemigos normales llevados a su mismo nivel (niveles 10, 30, 60 y 100), con el mejor equipo normal de su tipo para su nivel (`tools/sim.py`, `level_gear`) y también sin puntos o solo con el equipo inicial.

| Rol | Gana | Vida al terminar | Rondas |
|---|---|---|---|
| Ataque | 100 % | ~81 % | ~5 |
| Defensa | 100 % | ~78-83 % | ~9 |
| Curación | 100 % | ~85 % | ~10-12 |
| Soporte | 100 % | ~81 % | ~6-10 |

**Lo que no cumple D-110:**
1. **La defensa no aguanta más que el ataque:** recibe menos daño por ronda, pero tarda casi el doble en matar y termina con la misma vida o menos. En una pelea solo, un tanque hoy es un ataque más lento. Además, dos tanques tienen menos armadura base que su hermano de ataque (Guerrero 0,20 contra Furia 0,25; Protección 0,17 contra Reprensión 0,18).
2. **El equipo deja de mejorar en el nivel 8:** las piezas normales llegan al nivel de pieza 4 (pide nivel 8). Del 9 al 100 no hay equipo mejor que buscar; el bono del equipo es el mismo al 30 que al 100.
3. **Las peleas normales con equipo son demasiado fáciles a todo nivel** (100 % y ~80 % de vida): falta riesgo; el bestiario de nivel alto (en camino) y el equipo por niveles tienen que mover esto juntos.
4. **Lo que sí funciona:** los talentos suman de verdad (sin puntos, al nivel 30: 76-95 % de victorias y 34-50 % de vida; con puntos: 99-100 % y 60-69 %) y el equipo también (solo el inicial: ~63 % de vida; con el de su nivel: ~80 %).

**Lo que sigue:** ~~una pasada de balance con estos objetivos~~ **hecho** en la pasada de balance de clases y roles (más abajo, "pasada de balance de clases y roles (D-110)"): equipo de botín y de artesano cada 10 niveles hasta el 100 (lo mejor de cada nivel es de artesano, D-113), cada tanque con más armadura base que el ataque de su clase y con armadura que crece con sus puntos, la defensa que termina con 7 a 19 puntos más de vida que el ataque desde el nivel 50, la curación que es la que más vida deja, y peleas normales que dejan ~55-65 % de vida con el equipo de su nivel. Se mide con `tools/balance_report.py`.

### Octubre de 2026: los oficios encadenados, fase 1 (D-109)

**Por qué.** El dueño pidió oficios "como en World of Warcraft": recolectar → refinar → fabricar, que avanzar no dependa de una sola cosa y que 50 jugadores tengan tareas distintas (ver [Profesiones](../07-economia/profesiones.md) §0). Son números **nuevos**, propuestos por Claude; solo se movió uno de antes (el cinturón). Todavía no se midieron con jugadores.

**Números nuevos** (`content/balance.yaml` → `professions`, y `content/professions.yaml` para las recetas):

| Número | Valor | Por qué |
|---|---|---|
| Curva de rango (`rank_formula`) | experiencia total = 9 × (rango − 1)²; rango 100 = 88.209 | Gran Maestro en ~1 año de juego constante (§4 de Profesiones, la referencia es el 99 de RuneScape) |
| Rango máximo (`max_rank`) | 100 | §4 |
| Experiencia de oficio al recolectar (`gather_xp_per_unit`) | 1 por unidad (también la carne y la piel del desollador) | Un recolector dedicado llega al 100 en 9 a 11 meses: junta más por vuelta a medida que sube de nivel |
| Experiencia de oficio al refinar o fabricar (`xp` de cada receta) | 6 por vez al refinar (1 ⚡); 12 por pieza de equipo (2 ⚡); 6 vendas y poción de vida, 8 poción mayor | 6 por ⚡ en todos: con 40 ⚡ al día, 240 por día, rango 25 en ~3 semanas, 50 en ~3 meses, 100 en ~1 año |
| Unidad extra por rango (`rank_yield`) | 0,3 % por rango por unidad recolectada o por vez refinada (rango 50: 15 %; 100: 30 %) | "Los recolectores juntan un poco más con cada rango"; el especialista rinde más que quien hace de todo (D-57) |
| Raros (`rare_chance`, `rare_per_rank`, `rare.min_rank`) | desde el rango 10: 5 % por vuelta con materiales del oficio, +0,15 % por rango (18,5 % en el 100) | 2 a 7 💠 gemas o 🌸 flores por día para un dedicado; la Joyería pide 1 a 3 por pieza |
| Experiencia de héroe por ⚡ al refinar y fabricar (`hero_xp_per_energy`) | 20 × (1 + 0,15 × (nivel − 1)), nivel = el menor entre tu nivel y tu rango en ese oficio | D-108: ver la cuenta de abajo |
| Bono del campamento (`camp_bonus`) | +10 % de sacar una unidad más al refinar en tu 🧵 Taller o 🔨 Herrería | "Con algo más de rendimiento" (§0); chico, para no vaciar el Claro |
| Energía por receta (`energy`) | 1 ⚡ refinar, vendas, poción de vida y poción mayor; 2 ⚡ cada pieza de equipo y la tanda de pociones mayores | D-78: toda acción fuera del combate gasta energía |
| Recetas por página (`per_page`) y botón de tanda (`make_batch`) | 2 por página si son más de 3; 🔨 Hacer 5 | 4 botones como mucho (D-75) |
| Piel (`enemies.yaml` → `loot.piel`) | cada bestia, 10 puntos menos que su carne (30 a 50 %), 1 o 2 | La Curtiduría pide 2 por cuero; un cazador saca ~0,6 por bestia vencida |
| Precios de lo refinado (`items.yaml`) | tablón 7, lingote 13, extracto 10, tela 7, cuero 7 (piel 3, gema 15, flor 12) | En el mercader, lo que sale vale lo que entra: refinar no fabrica monedas |
| Equipo de artesano (`items.yaml`, `source: crafted`) | rango 1 = poco común del nivel 3; rango 25 = raro del nivel 5 + un bono; rango 50 = épico del nivel 8 + un bono | Como el botín de su nivel y algo más arriba, para que el artesano sea necesario; se vende al mercader por menos que sus materiales |
| 🍷 Poción mayor | cura 60 %, toxicidad 60, precio 18 | Más eficiente que la de vida (35 % por 40) pero una por pelea |

**Número movido:**

| Número | Antes | Ahora | Qué mueve |
|---|---|---|---|
| Cinturón (`hero.belt_slots`) | poción de vida 3, venda 2 | + **1 🍷 poción mayor** | Quien la fabrica o la consigue puede llevar una al combate. La toxicidad (tope 100) sigue limitando: una mayor y una de vida por pelea |

**Cuenta rápida: experiencia por ⚡ (D-108).** Con toda la energía cada día (40 ⚡) y la misma fórmula de niveles:

| Camino | Experiencia por ⚡ | Hasta el nivel 100 |
|---|---|---|
| Recolectar en tu territorio, sin peleas | 14 × escala del nivel | ~2,9 años (D-108) |
| Recolectar con sus peleas | ~20 × escala (14 + las peleas) | ~2,0 años (D-108) |
| **Refinar o fabricar** (dedicado, rango ≥ nivel) | **20 × escala** | **~2,0 años** |

Un artesano dedicado sube su rango más rápido que su nivel (rango 100 en ~1 año, nivel ~47 en ese tiempo), así que su "nivel de trabajo" es siempre su nivel y no lo frena. Quien llega de nivel alto y empieza un oficio en rango 1 gana 20 por ⚡: un novato aprende poco. Refinar en el Claro con madera juntada ahí mismo (zona de nivel 1, sin peligro) rinde cerca del 70 % de recolectar en una zona de tu nivel: lo seguro rinde menos, como el territorio propio.

**Lo que queda por mirar:** si 2 ⚡ por pieza de equipo es mucho o poco cuando llegue el mercado (y si conviene que la tanda cueste menos energía por pieza), si el rango 10 de los raros es demasiado pronto o tarde para la Joyería, cuánta piel entra al juego con la cacería (D-106), si los precios de lo refinado dejan algún hueco para ganar monedas, y el equipo de artesano cuando haya botín por encima del nivel 8 (**hecho** en la pasada de D-110: artesano cada 10 niveles hasta el 100, siempre algo mejor que el botín de su nivel).

### Octubre de 2026: el beneficio de cada oficio (D-111)

**Por qué.** El dueño pidió que cada oficio dé un beneficio propio a un tipo de jugador, que crezca con la experiencia, como en World of Warcraft. Son números **nuevos** (`content/professions.yaml` → `perk` de cada oficio) y crecen parejos con el rango: al 50, la mitad; al 100, el valor entero.

| Oficio | Al rango 100 | Solo si |
|---|---|---|
| 🪓 Leñador | +10 de espacio en la mochila | — |
| ⛏️ Minero | +5 % de vida | — |
| 🌿 Herbolario | vida que vuelve sola 20 % más rápido | — |
| 🔪 Desollador | +4 % de ataque | — |
| 🪑 Carpintería | +4 % de ataque (hasta la 0.20; desde D-116, la ✒️ obra maestra: ver el registro de abajo) | peleas con arco o bastón |
| 🔨 Herrería | +3 puntos de armadura (tope 60 %) | llevas placas |
| 🦺 Peletería | +4 % de ataque y +3 % de vida | llevas cuero o malla |
| 🪡 Sastrería | +5 % de ataque | llevas tela |
| ⚗️ Alquimia | pociones +30 % | — |
| 💍 Joyería | +3 % de vida y de ataque | — |
| 🩺 Medicina | curaciones +15 %; vendas, ungüentos y botiquines +30 % | lo primero, si eres sanador |

**Cuenta rápida:** un guerrero de placas con Minero, Herrería y Joyería al 100 suma +8 % de vida, +3 % de ataque y +3 puntos de armadura: lo mismo que una pieza de equipo de nivel mediano. Con todos los oficios al 100 (años de juego, D-57) un personaje de tela suma +12 % de ataque y +11 % de vida. Se revisa en la pasada de balance de D-110 y en P-76. **Medido en la pasada de D-110:** con todos los que le sirven al rango 100, de +1 a +7 puntos de vida al terminar las peleas comunes (escenario c de `tools/balance_report.py`): se nota sin reemplazar al equipo.

### Octubre de 2026: lo que respondió el dueño en la entrevista de voz (D-118, D-119, D-125, D-154)

**Por qué.** Respuestas del dueño (E-01, E-02, E-09, E-38). Números **confirmados**.

| Número | Antes | Ahora | Por qué |
|---|---|---|---|
| Ritmo al nivel 100 (`hero.xp_formula`) | ~2 años con toda la energía (1,8 medido) | **sin cambios** | El dueño eligió no acelerar (D-118); cierra P-77 |
| Retirada de las peleas automáticas (`auto_fight.defaults.retreat`) | 50 % | **30 %** | Con 50 % el lote se cortaba después de unas 4 peleas; con 30 % sigue casi entero y pierde menos del 1 % de las peleas (§ de ⚙️ Opciones, abajo) |
| Oleadas (`raids.per_week`, antes `interval_days: 7`) | 1 cada 7 días | **3 por semana** (cada ~2 días y 8 horas) | Más presión sobre el campamento: la despensa pierde el 25 % en cada oleada perdida, así que las defensas y la comida importan más (D-154; quizás 5 por semana más adelante) |
| Provisiones del mercader (`shop.weekly_cap`) | sin tope | **20 por jugador por semana** | La despensa la llenan los oficios (caza, pesca, cocina; D-125): el mercader es un salvavidas |

**Lo que queda por mirar:** con 3 oleadas por semana, cuántas pierde un campamento chico (1 o 2 activos) y si la despensa aguanta; si hace falta bajar `raids.loss_share` (25 %) para los campamentos que recién empiezan.

### Octubre de 2026: el Comercio, un oficio que no pelea (D-116)

| Número | Valor | Por qué |
|---|---|---|
| Beneficio del 💱 Comercio (`professions.yaml` → comercio.perk.sell) | +20 % de monedas al vender, al rango 100 (parejo con el rango) | Lo pidió el dueño: el comerciante cobra más, sin ventaja en combate |
| Experiencia de Comercio (`professions.trade_xp_per_coin`) | 1 por cada 🥉 de la venta base | Quien vende ~240 🥉 al día llega al rango 100 en ~1 año, como los demás oficios |

**Lo que queda por mirar:** el Comercio es una fuente de monedas (vender da hasta 20 % más). Si en la beta entra demasiado bronce, se compensa con el impuesto del mercado de órdenes (segunda tanda de la economía).

### Octubre de 2026: la obra maestra y los muebles del campamento (D-116)

**Por qué.** El dueño pidió que ser carpintero deje hacer piezas más exclusivas (D-116: los beneficios de oficio no son solo de combate). Números **nuevos** salvo el de la Carpintería, que cambia.

| Número | Antes | Ahora | Por qué |
|---|---|---|---|
| Beneficio de la 🪑 Carpintería (`professions.yaml` → carpinteria.perk) | +4 % de ataque con arco o bastón al rango 100 | **hasta 15 %** de obra maestra en sus arcos y bastones (`masterwork: 0.15`), parejo con el rango | Pasa de combate a exclusivo, como pide la tabla de §0.4 de [Profesiones](../07-economia/profesiones.md) |
| Obra maestra de los demás oficios de equipo (`masterwork.base_chance`) | — | hasta **5 %** por pieza al rango 100 (Herrería, Sastrería, Peletería, Joyería) | Que todo artesano pueda tener suerte, y el carpintero sea el especialista (3 veces más) |
| Bono de la obra maestra (`masterwork.stat_bonus`) | — | **+10 %** en cada bono de la pieza | Se nota: una obra maestra vale más o menos lo que la pieza normal del nivel siguiente (el arco firmado del nivel 90 da +40 % de ataque; el normal del 100, +39 %), sin pasar a la obra maestra de ese nivel |
| Bono de más (`masterwork.extra`) | — | arma +1 de defensa; pecho +2 % de ataque; joya +2 % de vida | "Un bono más", como dice la tabla del dueño |
| Precio (`masterwork.price_mult`) | — | **×1,25** sobre la pieza normal | "Vale más". Vender todo lo fabricado, con 15 % de obras maestras, rinde en promedio ~3,7 % más que el precio de sus materiales (la pieza normal, ~99,5 %): se acepta (cuesta energía y el mercado entre jugadores la pondrá en su precio) |
| 🛏️ Literas de roble (`items.yaml`, receta de rango 40) | — | **+1 lugar** de miembro; tablón ×12, tela ×4, cuero ×2; 4 ⚡ | Mueble exclusivo del carpintero; uno por campamento |
| 🗄️ Armero de roble (receta de rango 70) | — | **+1 de 🛡️ Defensa** (11 → 12 con todas las mejoras); tablón ×16, lingote ×6, cuero ×3; 4 ⚡ | Cada punto debilita 4 % a los atacantes de la oleada (`raids.defense_weaken_per_point`) |

**Cuenta rápida:** un carpintero de rango 100 que fabrica 20 arcos saca unos 3 firmados. Un cazador con un arco obra maestra del nivel 100 lleva +43 % de ataque en vez de +39 % y +1 de defensa: algo menos que el +4 % de ataque que daba antes el oficio, pero solo para quien tiene la pieza, y el carpintero puede venderla o regalarla cuando exista el mercado. **Lo que cambia en la medición de D-110:** en el escenario "c" de `tools/balance_report.py` (todos los oficios al 100) los que pelean con arco o bastón pierden el +4 % de ataque de la Carpintería (las obras maestras no entran en ese escenario). Medido con `tests/test_masterwork.py`: 200 piezas al rango 100 dan 32 obras maestras en la Carpintería (16 %) y 9 en la Herrería (4,5 %).

### Octubre de 2026: el 🧭 Explorador y los 👹 campamentos enemigos (D-112)

**Por qué.** El dueño pidió que explorar sea un oficio que muestre más del mapa con el rango y que haya campamentos enemigos que cambien de lugar cada día y no dejen explorar su zona (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.14). Son números **nuevos**, propuestos por Claude (`content/balance.yaml` → `explorer` y `enemy_camps`; el beneficio, en `content/professions.yaml` → explorador.perk). No se movió ningún número de antes.

| Número | Valor | Por qué |
|---|---|---|
| Experiencia de Explorador (`explorer.xp_per_step`, `xp_full_zone`) | 5 por vuelta de exploración y 6 más al dejar una zona al 100 % | ~6 por ⚡ (una zona se completa en ~4 vueltas), como refinar (6): rango 100 en ~1 año dedicado, con la curva de todos los oficios |
| Beneficio del Explorador (`perk.explore`) | +5 puntos de exploración por vuelta al rango 100 (+1 cada 20 rangos) | Como los demás beneficios (D-111): parejo con el rango y chico (una vuelta da 15 a 30) |
| Umbrales del mapa (`explorer.ranks`) | ⏱️ 10 · 👹 a 3 zonas 25 · 🕵️ 30 · 👹 todo el mapa 50 · 👹 fuerza 75 · 🏅 título 100 | La tabla de §1.14; el 10 llega en ~3 días de toda la energía, el 30 en ~1 mes |
| Lugares con su tiempo desde el rango 10 (`explorer.places_listed`) | 8 (sin rango, 3) | Lo que pidió el dueño ("qué tan lejos está"); los botones siguen en 3 |
| Campamentos por día (`enemy_camps.density`, `min_lejania`) | ~3 % de las zonas de Lejanía 2 o más (4 o 5 en un mapa de 13 × 13) | Que cada uno tenga alguno cerca sin llenar el mapa de zonas bloqueadas |
| Guarnición (`garrison`, `level_bonus`) | 4 a 8 enemigos contando al jefe, del nivel de la zona + 1 | Un día de trabajo para uno, una tarde para varios (§6.2 de supervivencia: nunca más de + 2) |
| Jefe (`chief_hp_mult`, `chief_attack_mult`) | El más fuerte del bioma, vida × 1,8 y ataque × 1,2 | Más difícil que un guardia sin pedir grupo (la Noche de prueba, pensada para varios, usa 2,0 y 1,3) |
| Energía de una pelea del asalto (`fight_energy`) | 2 ⚡ | Como una presa (D-108): la experiencia por ⚡ queda a la par |
| Cofre (`chest`) | nivel × 25 🥉, 3 a 5 materiales de la zona, 60 de experiencia × (1 + 0,15 × (nivel − 1)), 50 % de una pieza de equipo del nivel | Unas 15 peleas comunes de monedas; el equipo es el sorteo de botín de siempre con más probabilidad (las comunes: 15 %, 10 % desde el nivel 10), nunca de artesano |
| Parte de cada uno que peleó (`share`) | nivel × 8 🥉 y 30 de experiencia × (1 + 0,15 × (nivel − 1)) | Como una pelea más; huir no cuenta |
| Infiltrarse (`infiltrate`) | 3 ⚡; te descubren 45 % al rango 30 y 0,5 puntos menos por rango (10 % al 100, mínimo 5 %); +10 % de exploración y 15 de experiencia de Explorador | 5 de oficio por ⚡, como explorar; una vez por campamento y día |

**Medido con el motor** (`tools/balance_report.py`: `kit_for` y `fight`, 45 especializaciones, los 8 biomas con peligro, 2 peleas por bioma; el jefe es el más fuerte del bioma al nivel de la zona + 1 con vida × 1,8 y ataque × 1,2; el guardia, uno de la lista del bioma al nivel + 1):

| Zona | Kit | Gana al jefe | Gana al guardia | Vida al terminar con el guardia |
|---|---|---|---|---|
| 3 | equipo de inicio, sin puntos (a) | 38 % | 98 % | 51 % |
| 3 | puntos y botín de su nivel (b) | 85 % | 100 % | 67 % |
| 5 | b | 85 % | 100 % | 66 % |
| 10 | b | 97 % | 100 % | 65 % |
| 30 | b | 88 % | 100 % | 60 % |
| 60 | b | 95 % | 100 % | 69 % |

Sin puntos ni equipo de su nivel, el jefe es casi imposible desde la zona 5 (10 %, y 0 % en la 30): el campamento premia a quien ya juega su nivel. Con el kit de su nivel, una pelea del asalto deja ~65 % de vida, como una pelea común (C-21).

**Experiencia por ⚡ frente a D-108.** Una pelea del asalto es del nivel + 1: en una zona de nivel 3, un lobo da 30 × 1,45 = 43 por 2 ⚡ (~22 por ⚡) contra ~20 de cazarlo en la misma zona (un 10 % más; un 4 % en una zona de nivel 10). Un campamento de 6 en solitario (5 guardias, el jefe y el cofre) da 6 × 43 + 87 = 348 por 12 ⚡ (~29 por ⚡), y ~22 contando los ~4 ⚡ del viaje para llegar: a la par de D-108, porque cada campamento cae una sola vez por día y se reparte entre todos los que pelean.

**Lo que queda por mirar:** si 3 % deja demasiadas zonas bloqueadas cerca de los campamentos de jugadores (medir cuántas veces por día un jugador encuentra su zona bloqueada); si el cofre (50 % de equipo) hace que los campamentos rindan más que cazar para el equipo (D-113 pide que lo mejor lo fabriquen los jugadores: el cofre da el botín común de su nivel, nunca equipo de artesano); si el jefe de los anillos lejanos debería pedir grupo.

### Octubre de 2026: ⚙️ Opciones y peleas automáticas en los lotes (D-114)

**Por qué.** El dueño pidió que, si sale una pelea en medio de un lote, el jugador pueda elegir antes si el héroe la pelea solo o si se corta para pelearla él, con un botón de opciones (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.12.1). La forma de jugar sola se mudó del simulador al motor (`engine/combat/auto.py`), así hay **una sola**: la de las peleas automáticas es la que mide el simulador. Los números de las opciones y de la cacería en lote son **nuevos**, propuestos por Claude; los umbrales de la forma de jugar **no cambiaron**: son los que el simulador ya tenía escritos en su código y ahora viven en `balance.yaml`.

**Números nuevos** (`content/balance.yaml` → `auto_fight` y `hunt`):

| Número | Valor | Por qué |
|---|---|---|
| Opciones por defecto (`auto_fight.defaults`) | ✋ Manual, 50 %, pociones sí | Nada cambia para quien no toca ⚙️ Opciones (también los héroes de antes) |
| 🩹 Retirarse con menos de (`auto_fight.retreat_choices`) | 30, 50 o 70 % de vida | Tres escalones fáciles de entender: arriesgado, normal, prudente |
| Tope de rondas (`auto_fight.max_rounds`) | 60, y la pelea se deja sin premio ni castigo | El mismo tope que el simulador; ninguna pelea medida llega ahí, es solo para que siempre termine |
| Forma de jugar (`auto_fight.policy`) | curar < 45 % · poción < 35 % · venda < 30 % · golpe grande > 1,5 · 🌀 Esquivar ≥ 2 · curación lenta < 80 % · curar al final < 60 % · rematar con 3 combos | Los mismos de `tools/sim.py` desde D-79 (movidos, no cambiados) |
| Energía de cazar en lote (`hunt.batch`) | ⚡ 4, 10, 20, 40 o todo (2, 5, 10 o 20 presas) | Las mismas cantidades que explorar y recolectar, en pares porque cada presa cuesta 2 (D-108) |
| Tiempo por presa en lote (`hunt.batch_minutes`) | 16 minutos | 8 min por ⚡, como recolectar; cazar de a una, a mano, sigue siendo enseguida (el jugador atento va más rápido) |

**Paridad del simulador.** Con la forma de jugar ya en el motor, `tools/sim.py --summary`, `--summary --real`, `--boss --seeds=30` y `--bars --level=10` dieron **exactamente** los mismos números que antes (comparado línea por línea). La única diferencia de la versión del motor es que con otras pociones en el cinturón (🍷 poción mayor) elige la que más cura sin pasarse de lo que falta; el simulador solo lleva 🧪 de vida y 🩹 vendas, así que no cambia.

**Medido con el motor** (las especializaciones con el kit real, contra los enemigos de nivel 1 a 3 del bestiario por niveles, cinturón de inicio, 20 peleas cada una):

| Forma de jugar | Gana | Vida al terminar (si gana) | Victorias que terminan bajo 50 % |
|---|---|---|---|
| Básica (el simulador de siempre) | 100 % | 66 % | 16 % |
| Atenta (las peleas automáticas) | 99,9 % | 65 % | 17 % |

**Cuántas peleas dura un lote** (héroe de nivel 2 al lado del Claro, la vida vuelve sola en 4 horas, D-103):

| Límite de 🩹 Retirarse | Explorar 20 veces | Cazar 20 presas | Derrotas |
|---|---|---|---|
| 30 % | ~10 peleas (casi todo el lote) | ~16 presas | < 1 % |
| 50 % (por defecto) | ~4 peleas | ~5 presas | 0 % |
| 70 % | ~2 peleas | ~2 presas | 0 % |

**Cuenta rápida.** Pelear solo da lo mismo que pelear a mano (mismas reglas, sorteo y final), así que la experiencia por ⚡ de cada camino (D-108) no cambia. Lo que cambia es el ritmo con el chat cerrado: con 50 %, un lote largo se corta pronto porque cada pelea quita cerca de un tercio de la vida y la vida tarda 4 horas en volver. Cazar en lote a 16 min por presa y 2 ⚡ (40 ⚡ = 20 presas = 5 h 20 min) no sube la experiencia por día: la energía sigue siendo el tope.

**Lo que queda por mirar:** si 50 % por defecto corta los lotes demasiado pronto para el que sale y vuelve (con 30 % casi todo el lote se juega y las derrotas siguen bajo 1 %: si los jugadores se quejan de lotes cortos, bajar el valor por defecto a 30 %); si las peleas automáticas hacen que nadie juegue a mano (medir en la beta qué porcentaje elige ⚔️ Automática); y si 16 minutos por presa es mucho o poco frente a cazar a mano.

### Octubre de 2026: pasada de balance de clases y roles (D-110)

**Por qué.** El dueño pidió (D-110, confirmada) que las clases funcionen de verdad y no "para bonito": cada especialización rinde según sus estadísticas y su rol, y todo lo que se mejora suma (niveles, talentos, equipo, mejoras del campamento y oficios). Con D-113 (provisional), lo mejor de cada nivel lo fabrican los jugadores y el botín suelta menos y peor. D-108 (confirmada) no se toca: cada camino llega al nivel 100 en ~2 años con toda la energía. La corrida de diagnóstico de arriba dijo qué no cumplía; esta pasada lo corrige.

**Cómo se midió.** Con `tools/balance_report.py` (nuevo; usa la forma de jugar del motor, la misma de las peleas automáticas de D-114): las 45 especializaciones, a los niveles 1, 10, 25, 50, 75 y 100, contra **todos** los enemigos comunes que caben en ese nivel (de cualquier bioma), al mismo nivel, con juego atento y cinturón lleno (3 🧪 y 2 🩹; la toxicidad deja beber 2 pociones por pelea), 8 peleas por enemigo. Escenarios:
- **a** = equipo inicial (arma y pecho de nivel 1) y sin puntos de talento.
- **b** = el kit de verdad: nivel − 1 puntos en la especialización (barra automática y pasivas) y, en las 7 ranuras, la mejor pieza de **botín** de su tipo para su nivel. Es la referencia.
- **c** = b + la mejor pieza de **artesano** de su nivel donde la hay (arma, pecho y joya) + todos los beneficios de oficio que le sirven, al rango 100 (D-111).
- **b3** = b contra los enemigos de 3 niveles más.

Además: `--boss` (el Guardián al nivel 6, como siempre), `--trial` (la Noche de prueba por bioma y nivel de zona), `--sources` (qué suma cada mejora) y `--pace` (el ritmo de D-108). Para comparar se puede medir otra copia del contenido con `--content=<carpeta>`. Al nivel 1 nadie tiene especialización todavía (D-68): esa columna mide las estadísticas base de cada una.

**Resultado (escenario b, mediana de cada rol: gana % / vida al terminar % / rondas):**

| Rol | Nivel 10 | Nivel 25 | Nivel 50 | Nivel 75 | Nivel 100 |
|---|---|---|---|---|---|
| ⚔ Ataque | 100/75/7,0 → **100/67/7,4** | 100/69/8,1 → **100/51/9,2** | 100/72/6,2 → **100/59/6,6** | 100/66/8,0 → **100/57/8,4** | 100/64/7,2 → **100/59/7,5** |
| 🛡 Defensa | 100/72/9,4 → **100/65/9,6** | 100/64/12,1 → **100/60/12,2** | 100/72/11,1 → **100/73/11,6** | 100/69/13,5 → **100/72/13,7** | 100/67/13,5 → **100/72/12,7** |
| ✚ Curación | 100/84/14,7 → **100/78/16,0** | 100/81/16,4 → **100/64/19,6** | 100/79/11,6 → **100/76/13,1** | 100/79/13,9 → **100/78/15,2** | 100/79/14,5 → **100/77/15,0** |
| ✦ Soporte | 100/74/11,5 → **100/68/12,8** | 100/67/8,8 → **100/55/10,4** | 100/73/7,9 → **100/64/9,0** | 100/67/9,7 → **100/62/10,6** | 100/65/10,4 → **100/63/11,0** |

- **Orden de los roles, desde el nivel 25:** el ataque mata en menos rondas y termina con menos vida; el soporte queda en medio; la defensa termina con más vida que el ataque aunque tarde ~1,3-1,8 veces más; la curación es la que más vida deja y la que más tarda (~2 veces). Al nivel 10 (3 habilidades) la defensa todavía queda pareja con el ataque: subirla ahí haría trivial al Guardián del nivel 6 (ver abajo).
- **Algo de riesgo:** con el equipo de su nivel, el ataque termina con 51-59 % de vida (antes 64-72 %); la peor especialización gana el 98 % (Nigromante Plaga al nivel 25) y todas las demás el 98-100 %. Gana casi siempre porque las 2 pociones y 2 vendas devuelven ~100 % de vida: para bajar a 90-97 % de victorias habría que dejar ~40 % de vida por pelea, demasiado con la vida que vuelve en 4 horas (D-103). El riesgo se ve en la vida y en b3.
- **Más difícil 3 niveles arriba (b3):** al 10, 25 y 50 el ataque baja a 47-55 % de vida (antes 61-69 %), con la peor especialización entre el 92 y el 100 %.

**La defensa contra el ataque de su clase** (vida al terminar, escenario b, puntos de diferencia; antes → ahora):

| Clase: defensa − ataque | L10 | L25 | L50 | L75 | L100 |
|---|---|---|---|---|---|
| guerrero − guerrero_furia | −1 → **+4** | −19 → **+5** | −10 → **+12** | −14 → **+11** | −14 → **+15** |
| paladin_proteccion − paladin_reprension | −4 → **−1** | −2 → **+12** | −7 → **+7** | −8 → **+9** | −2 → **+9** |
| caballero_muerte_sangre − caballero_muerte_escarcha | −1 → **−1** | −4 → **+6** | +10 → **+15** | +12 → **+17** | +15 → **+12** |
| brujo_demonologia − brujo_destruccion | −4 → **−1** | −13 → **+3** | −5 → **+14** | −12 → **+9** | −12 → **+8** |
| monje_maestro_cervecero − monje_viajero_viento | −1 → **0** | −1 → **+12** | +3 → **+9** | +9 → **+19** | +3 → **+8** |
| druida_guardian − druida_feral | −4 → **−3** | −2 → **+2** | +13 → **+18** | +11 → **+15** | +13 → **+18** |
| cazador_demonios_venganza − cazador_demonios_estrago | −6 → **−4** | +6 → **+13** | −9 → **+9** | −9 → **+10** | −17 → **+7** |
| nigromante_legion − nigromante_plaga | −3 → **−4** | +6 → **+4** | +15 → **+17** | +19 → **+16** | +19 → **+16** |

**Los otros escenarios (mediana de vida al terminar, ataque / defensa / curación / soporte):**

| Escenario | Nivel 10 | Nivel 50 | Nivel 100 |
|---|---|---|---|
| a: equipo inicial, sin puntos | 45/47/30/48 → **30/33/12/31** (gana 78-86 %, curación 38 %) | 24/27/9/24 → **1/3/0/2** (gana ≤10 %) | 10/12/2/9 → **0/0/0/0** |
| b: botín de su nivel y sus puntos | 75/72/84/74 → **67/65/78/68** | 72/72/79/73 → **59/73/76/64** | 64/67/79/65 → **59/72/77/63** |
| c: + artesano + oficios al 100 | 81/79/89/80 → **76/75/85/76** | 78/79/84/79 → **71/82/79/74** | 73/72/83/73 → **71/82/82/74** |

**¿Suma todo? (`--sources`, mediana del rol: gana / vida, ataque · defensa · curación · soporte)**

| Variante | Nivel 10 | Nivel 50 |
|---|---|---|
| Sin puntos, sin equipo | 68/25 · 77/28 · 28/9 · 75/27 | 3/1 · 6/2 · 0/0 · 6/1 |
| Sin puntos, equipo inicial | 80/30 · 88/34 · 39/12 · 88/33 | 6/1 · 11/3 · 1/0 · 6/2 |
| Con puntos, equipo inicial | 96/44 · 99/45 · 95/54 · 100/45 | 33/9 · 100/49 · 70/27 · 81/27 |
| Con puntos, botín de su nivel | 100/68 · 100/66 · 100/78 · 100/68 | 100/59 · 100/73 · 100/77 · 100/64 |
| Con puntos, artesano | 100/70 · 100/69 · 100/79 · 100/71 | 100/65 · 100/77 · 100/78 · 100/69 |
| Con puntos, artesano y oficios al 100 | 100/76 · 100/76 · 100/84 · 100/76 | 100/71 · 100/82 · 100/79 · 100/75 |

Cada mejora suma: los puntos de talento (y sus habilidades), el equipo inicial, el botín de su nivel, el de artesano (+1 a +6 puntos de vida al terminar) y los beneficios de oficio (+1 a +7). Las defensas del campamento suman en las oleadas (tabla de la Noche de prueba). Antes, al nivel 50, el botín de su nivel y el artesano casi no se distinguían (era el mismo equipo del nivel 8).

**Números movidos.**

*Enemigos* (`content/enemies.yaml`, los 104 comunes; el Guardián no cambia):

| Número | Antes | Ahora | Qué mueve |
|---|---|---|---|
| Vida que suma cada nivel | `per_level.hp` | × **1,3** desde el nivel 3 (la base baja 0,6 × lo de antes para que al nivel 3 quede igual) | Peleas algo más largas desde el nivel 4; los niveles 1 y 2, algo más fáciles |
| Ataque que suma cada nivel | `per_level.attack` | × **1,8** desde el nivel 3 (la base baja 1,6 × lo de antes) | Con el equipo de su nivel, ~55-65 % de vida al terminar en vez de ~80 %. Al nivel 50 un bruto pega ~1,7 veces más que antes y tiene ~1,3 veces más vida; al 100, igual |
| Experiencia, monedas, botín, golpes | — | sin cambios | El ritmo de D-108 solo cambia por las derrotas (cuenta abajo) |

*Talentos* (`content/balance.yaml` → `talents.passive`, por punto, hasta 50 puntos):

| Rol | Antes | Ahora | Qué mueve |
|---|---|---|---|
| 🛡 Defensa | +1 % de vida | **+1,25 % de vida y +0,2 de armadura** (nuevo: `armor`, que `hero_stats` suma a la armadura sin pasar el tope de 60 %) | La defensa aguanta más a medida que sube (al 50: +62 % de vida y +10 de armadura); al nivel 6 suma solo +1 de armadura, así el Guardián casi no cambia |
| ✚ Curación | +0,6 % de vida y +0,4 % de ataque | **+0,85 %** de vida y +0,4 % de ataque | La curación es el rol que más vida deja. Sigue en 1,25 % por punto (`tests/test_spec_abilities.py`: talentos chicos al nivel 5) |
| ✦ Soporte | +0,6 % de ataque y +0,4 % de vida | **+0,5 % de ataque y +0,6 % de vida** | El soporte queda entre el ataque y la defensa también en la vida |
| ⚔ Ataque | +1 % de ataque | sin cambios | — |

*Barra automática* (`engine/classes/talents.py`): en las especializaciones de 🛡 Defensa, la casilla 3 es su **curación más nueva**, si ya abrió alguna (antes, "la otra habilidad más nueva", que al nivel 25 sacaba la curación de 5 de los 8 tanques). Quien eligió su barra no cambia. El texto de 🎛️ Barra de combate lo dice.

*Equipo* (`content/items.yaml`, `content/balance.yaml` → `gear`):

| Número | Antes | Ahora | Qué mueve |
|---|---|---|---|
| Niveles de pieza del botín | 4, hasta el nivel 8 (común → épico) | **14**: 1-4 como antes y del 5 al 14 en los niveles 10, 20 … 100, en las 7 ranuras y los 4 tipos de armadura y de arma (250 piezas nuevas) | El equipo sigue mejorando hasta el 100. Del nivel 8 al 100, el arma pasa de +17 % a +35 % de ataque, el pecho de +20 % a +40 % de vida (y +4 → +6 de armadura), la joya de +11/+8 % a +21/+16 %; con las 7 ranuras, de +29 % de ataque, +61 % de vida y +10 de armadura a +61 %, +124 % y +15 (con arma, pecho y joya de artesano: +71 %, +135 % y +19) |
| Rareza del botín desde el nivel 10 | — | como mucho **🔵 raro** (D-113) | Se ve que el botín es "de menos calidad" |
| Equipo de artesano | 3 niveles (3, 5, 8), solo arma, pecho y joya | **13**: +10 niveles (10 … 100), 🟣 épicos, con ~10 % más que el botín de su nivel y un bono (vida en las armas, ataque en el pecho, defensa en la joya). 90 piezas nuevas | En cada nivel, desde el 3, la mejor arma, pecho y joya son de artesano (`tests/test_balance_d110.py`) |
| Equipo de artesano del rango 1 | igual que el botín poco común del nivel 3 | **+1** de vida (armas), de ataque (pecho) o de defensa (joya) | Lo mejor de cada nivel lo fabrican los jugadores también al empezar (D-113) |
| Precios | botín 8 / 20 / 45 / 90 | botín de los niveles nuevos: **90 + 40 por nivel de pieza** en arma, pecho y joya (68 + 30 en las demás); artesano **+15 %** | Al mercader se vende a la mitad; el de artesano siempre por menos que sus materiales |
| Probabilidad de soltar equipo (`gear.high_level_drop`) | 15 % siempre | 15 % hasta el nivel 9, **10 %** desde el 10 (también la base del bono de la partida de caza) | El botín suelta menos (D-113) |
| Ventana de nivel del botín (`gear.level_window`) | −4 a +1; sin piezas, nada (desde el nivel 13 no caía equipo) | igual, y si cae entre dos niveles de pieza, **el más cercano por debajo** (`roll_gear`) | Las franjas altas vuelven a soltar equipo de su nivel |

*Oficios* (`content/professions.yaml`): **90 recetas nuevas**, una por nivel de pieza y línea (bastón, arco, espada, daga, peto, túnica, jubón, cota, joya), en los rangos **55, 60 … 100** (un nivel de pieza cada 5 rangos: nivel 10 → rango 55 … nivel 100 → rango 100). Piden lo refinado de 2 ramas o más y, en los niveles altos, más 💠 gemas y 🌸 flores de luna (ver [Profesiones](../07-economia/profesiones.md) §0.1). 2 ⚡ y 12 de experiencia de oficio, como las demás piezas: el ritmo de D-108 de quien fabrica no cambia. En 🛠️ Fabricar, las recetas de rango más alto salen primero.

*Especializaciones* (`content/classes.yaml`, 31 de 45). Criterio: la **armadura base** de cada tanque supera la del ataque de su clase; la **vida por nivel** acerca a cada especialización al objetivo de su rol (ataque ~55 %, soporte ~61 %, defensa ~69 %, curación ~74 % de vida al terminar, de los niveles 25 al 100) y el **ataque por nivel** de tanques y sanadores muy lentos los acerca a ~1,5 y ~2 veces las rondas del ataque. Cuando cambia lo que suma cada nivel, la base se mueve para que al nivel 6 (el Guardián) quede igual (al 3, en las de curación y soporte que perdían contra el Oso de las cumbres): solo cambian los niveles altos. Cada número lleva su nota `[ES]` en el archivo.

| Especialización | Rol | Cambios |
|---|---|---|
| guerrero_furia | Ataque | vida base 165 → 188; ataque base 15 → 16,5; armadura base 0,25 → 0,21; vida por nivel 13 → 8,5; `regeneracion_enfurecida` 0,25 → 0,15 |
| guerrero | Defensa | vida base 161 → 141; ataque base 11 → 10,5; armadura base 0,20 → 0,22; vida por nivel 15 → 19; ataque por nivel 1,4 → 1,5 |
| paladin_reprension | Ataque | vida base 139 → 154; armadura base 0,18 → 0,16; vida por nivel 14 → 11 |
| paladin_sagrado | Curación | vida base 105 → 100; vida por nivel 13 → 14 |
| cazador_punteria | Ataque | vida base 122 → 142; ataque base 13 → 13,5; vida por nivel 12 → 8; ataque por nivel 1,7 → 1,6 |
| picaro_sutileza | Soporte | vida base 110 → 104; vida por nivel 14 → 17 |
| picaro_forajido | Soporte | vida base 143 → 140; vida por nivel 13 → 14,5 |
| sacerdote_sombra | Ataque | vida base 122 → 107; vida por nivel 11 → 14 |
| sacerdote_sagrado | Curación | vida base 100 → 105; ataque base 10 → 9,2; vida por nivel 11 → 10; ataque por nivel 1,3 → 1,45 |
| caballero_muerte_sangre | Defensa | vida base 135 → 145; vida por nivel 15 → 13 |
| caballero_muerte_profano | Soporte | vida base 162 → 172; vida por nivel 14 → 12 |
| chaman_restauracion | Curación | vida base 110 → 125; ataque base 10 → 9,2; vida por nivel 12 → 9; ataque por nivel 1,3 → 1,45 |
| chaman_totems | Soporte | vida base 150 → 160; vida por nivel 13 → 11 |
| mago_fuego | Ataque | vida base 130 → 140; vida por nivel 11 → 9 |
| mago_escarcha | Soporte | vida base 121 → 119; vida por nivel 14 → 15 |
| mago_arcano | Soporte | vida base 143 → 135; vida por nivel 11 → 15 |
| brujo_destruccion | Ataque | vida base 100 → 105; vida por nivel 11 → 10 |
| brujo_demonologia | Defensa | vida base 144 → 119; ataque base 11 → 10,2; vida por nivel 14 → 19; ataque por nivel 1,4 → 1,55 |
| brujo_afliccion | Soporte | vida base 124 → 120; vida por nivel 11 → 13 |
| monje_maestro_cervecero | Defensa | vida base 125 → 140; ataque base 11 → 10; vida por nivel 14 → 11; ataque por nivel 1,4 → 1,6 |
| monje_tejedor_niebla | Curación | ataque base 10 → 9,8; ataque por nivel 1,3 → 1,4 |
| druida_feral | Ataque | vida base 110 → 95; vida por nivel 12 → 15 |
| druida_guardian | Defensa | vida base 135 → 125; ataque base 11 → 10,5; vida por nivel 15 → 17; ataque por nivel 1,4 → 1,5 |
| cazador_demonios_venganza | Defensa | vida base 125 → 105; ataque base 11 → 9,5; vida por nivel 14 → 18; ataque por nivel 1,4 → 1,7 |
| evocador_preservacion | Curación | vida base 110 → 108; vida por nivel 12 → 13 |
| evocador_aumentacion | Soporte | vida base 150 → 143; vida por nivel 12 → 15,5 |
| nigromante_plaga | Ataque | vida base 110 → 102; vida por nivel 11 → 12,5 |
| nigromante_legion | Defensa | vida base 125 → 142; vida por nivel 14 → 10,5 |
| bardo_duelista | Ataque | vida base 110 → 98; vida por nivel 12 → 14,5 |
| bardo_trovador | Curación | vida base 107 → 105; vida por nivel 12 → 13 |
| bardo_estratega | Soporte | vida base 143 → 140; vida por nivel 13 → 14,5 |

Las cinco con poca vida del informe del bestiario (Mago Arcano, Druida Feral, Bardo Duelista, Nigromante Plaga y Pícaro) quedan cerca de la mediana de su rol con el equipo de su nivel (43-60 % de vida del 25 al 100, 98-100 % de victorias; antes, con equipo de nivel 1, ganaban solo el 30-55 % contra los brutos de las franjas altas). Con equipo de nivel 1 en las 7 ranuras a nivel alto ahora **todos** pierden mucho (escenario `p1`: al nivel 50, el ataque gana el 58 %; al 100, el 14 %): con el equipo por niveles, quedarse con el equipo del comienzo ya no alcanza.

**Lo que no cambió (y se comprobó):**
- **El Guardián** (`--boss`, nivel 6, equipo hasta poco común, 100 peleas): todas entre el **53 %** (Guerrero Furia) y el **89 %** (Paladín Protección); antes, 54-84 %. Sigue en 45-90 %.
- **Las primeras peleas** (`tools/sim.py --summary --real`, enemigos de nivel 1 a 3): la peor sigue en **90 %** (Bardo Trovador contra el Oso de las cumbres); las de curación, 90 % o más.
- **El ritmo de D-108** (`--pace`): solo con la experiencia, el nivel 100 llega en **1,82 años** (la experiencia de los enemigos no cambió); con las derrotas del escenario b, 1,82 (la media) y 1,85 (la peor especialización). `tests/test_bestiary.py` lo mantiene entre 1,7 y 2,1. Lo que no entra en la cuenta: con ~55-65 % de vida por pelea, hace falta curarse más seguido (pociones, la posada, la vida que vuelve en 4 h); las peleas automáticas de D-114 cortan el lote por debajo del 50 %.

**La Noche de prueba** (`--trial`: el enemigo más fuerte del bioma al nivel de la zona + 2, con vida × 2 y ataque × 1,3; media de los 8 biomas, % de victorias de las 45 especializaciones; antes → ahora). `raids.trial` no cambió:

| Zona | Equipo | Sin defensa | 🛡️ 4 puntos | 🛡️ 11 puntos |
|---|---|---|---|---|
| 5 | inicial (1) | 34 → **11** | 61 → **35** | 100 → **99** |
| 5 | poco común | 48 → **24** | 85 → **55** | 100 → **99** |
| 5 | botín de su nivel | 72 → **44** | 96 → **81** | 100 → **100** |
| 15 | inicial (1) | 48 → **3** | 87 → **15** | 100 → **92** |
| 15 | botín de su nivel | 98 → **54** | 100 → **87** | 100 → **100** |
| 30 | botín de su nivel | 97 → **69** | 100 → **94** | 100 → **100** |
| 60 | botín de su nivel | 97 → **82** | 100 → **99** | 100 → **100** |
| 90 | inicial (1) | 43 → **2** | 76 → **10** | 100 → **80** |
| 90 | botín de su nivel | 94 → **87** | 100 → **99** | 100 → **100** |

"Cerca de la mitad" (D-99) vale ahora para quien defiende con el equipo de su nivel en las zonas de 5 a 15 (44-54 %; antes lo daba el equipo inicial, 34-48 %, porque el equipo no crecía). En zonas de nivel 30 o más se gana el 69-87 %, y con las defensas del campamento casi siempre. Con el equipo inicial ya casi no se gana.

**Lo que queda por mirar (o por decidir):**
- **Victorias:** con juego atento y el cinturón lleno se gana el 98-100 % de las peleas comunes; el riesgo está en la vida que queda. Si el dueño quiere 90-97 % de victorias, hay que dejar ~40 % de vida por pelea (más duro con la vida en 4 h). Propuesta: dejarlo así.
- **Quien nunca se cambia el equipo:** con el equipo inicial, desde el nivel ~20 pierde mucho. D-83 dice que lo nuevo solo se pone solo en una ranura vacía; conviene avisar "tienes una pieza mejor" (o que el dueño decida si lo mejor se pone solo).
- **La Noche de prueba en zonas altas** queda más fácil que en las bajas con el equipo de su nivel: si molesta, que `raids.trial` crezca con el nivel de la zona.
- **Artesano en cabeza, manos, piernas y pies:** todavía solo hay botín en esas 4 ranuras; lo mejor de cada nivel es de artesano en arma, pecho y joya. Van con la segunda tanda de la economía (D-113: durabilidad y pedidos).
- **El nivel 10:** la defensa queda pareja con el ataque (−4 a +4 puntos) porque el Guardián del nivel 6 frena subirla antes.
- `tools/balance_report.py` tarda ~20 s el informe completo con 4 procesos; el modo `--trial`, ~1 minuto.

### Octubre de 2026: historia, encargos y facciones (D-117, provisional)

**Por qué.** El dueño pidió que el juego sea largo por su historia y su rol, no por subir despacio (ver [Historia y rol](../06-contenido/historia-y-rol.md) §0). La historia paga experiencia, monedas, reputación y cosas, así que sus números entran aquí. Son **nuevos**, propuestos por Claude; no se movió ningún número de antes (tampoco `hero.xp_formula`: la velocidad de los niveles sigue en P-77). Se ajustan en la beta.

**Números nuevos** (`content/balance.yaml` → `story`; premios de cada misión y encargo en `content/story.yaml`):

| Número | Valor | Por qué |
|---|---|---|
| Experiencia de misión por ⚡ (`story.xp_per_energy`) | 20 × los ⚡ que pide la misión (`energy`) × (1 + 0,15 × (nivel de la misión − 1)) | Lo mismo que da explorar por ⚡ (D-104, D-108): mientras haces la historia rindes el doble, pero cada misión se cobra una sola vez. La escala es la de matar y recolectar (`hero.xp_level_scale`) |
| Experiencia de encargo por ⚡ (`story.task_xp_per_energy`) | 10 × ⚡ del encargo × (1 + 0,15 × (nivel del héroe − 1)) | La mitad, porque se repiten cada día |
| Monedas del encargo (`story.task_coins_per_level`) | 8 a 12 🥉 × (1 + 0,1 × (nivel − 1)) | Como el oro de las peleas (+10 % por nivel) |
| Encargos de campamento (`story.camp_tasks`, premio en `story.yaml`) | 2 por semana; 60 exp y 30 🥉 a cada miembro que aportó | Algo más que el premio de la partida de caza (40 y 20): es una semana de trabajo entre todos |
| Rangos de reputación (`story.ranks`) | Conocido 100 · Apreciado 300 · Honrado 700 · Héroe 1.500 | Conocido con el Capítulo 1; Apreciado en ~3-4 semanas de encargos; Héroe, meta de meses |
| Rasgos de origen (`story.yaml` origins) | +15 % de experiencia de un oficio de recolección, +10 % en refinado y fabricación, −10 % en el mercader o +10 % de reputación | Chicos y nunca de combate (D-49) |

**Cuenta rápida.**
- **Capítulo 1:** 7 misiones, 57 ⚡ de actividades, ~1.500 de experiencia de premio (100, 80, 138, 229, 156, 348 y 448), 140 🥉 y las monedas de las decisiones (hasta 150). Un origen: 15 a 18 ⚡, 354 a 420 de experiencia y 35 🥉 (más su regalo).
- Juntos, ~1.900 de experiencia: un 16 % de lo que pide el nivel 8 (11.618). La experiencia de las acciones mismas (explorar, recolectar, pelear) se cobra aparte, como siempre.
- **Encargos:** 3 por día, de 2 a 6 ⚡ cada uno. Al nivel 1 pagan 20 a 60 de experiencia: unos 120 al día, contra ~800 de un día entero de energía (40 ⚡ × ~20). Es un +15 % al ritmo diario, igual para todos los caminos (cuentan explorar, recolectar, pelear, cazar, fabricar y vender).
- **Monedas que entran:** ~30 🥉 por día en encargos al nivel 1; los premios de rango son cosas que ya existen (consumibles, materiales) y algo de monedas en la Cofradía (50, 150 y 500 🥉, una sola vez).

**Lo que queda por mirar:** si el +15 % diario de los encargos acelera demasiado la subida (D-108 pide caminos parejos; si pasa, bajar `task_xp_per_energy`); si las misiones de "ganar peleas" de los orígenes y del capítulo son muy duras al nivel que piden; si Apreciado llega demasiado pronto o tarde con un encargo por facción al día; y si los premios de rango de la Cofradía (monedas) pesan más que los de las otras dos.

### Octubre de 2026: ✨ Encantamiento, la pieza mejor y el artesano de cabeza, manos, piernas y pies (fase 2 de D-115, provisional)

**Por qué.** El dueño pidió tantos oficios como hagan falta, conectados entre sí (D-115). La fase 2, lado del equipo, cierra el ciclo del equipo de la [Red de oficios](../07-economia/red-de-oficios.md) §4: el artesano hace todas las ranuras y el encantador desencanta lo viejo y mejora lo nuevo. La pasada de balance (D-110, D-113) había dejado cabeza, manos, piernas y pies solo con botín. Números **nuevos** (nada movido), propuestos por Claude y a ajustar en la beta.

| Número | Valor | Por qué |
|---|---|---|
| ✨ Esencias al desencantar (`enchanting.disenchant`) | ⚪ 1 · 🟢 2 · 🔵 3 · 🟣 4, +1 cada 20 niveles de la pieza; 🔮 1 esencia mayor de las 🟣 épicas; 1 ⚡ y 6 de experiencia de oficio | Una pieza vieja rinde más cuanto mejor era; la esencia mayor obliga a pasar por el artesano (las épicas son suyas desde el nivel 10) |
| Beneficio del ✨ Encantamiento (`professions.yaml` → encantamiento.perk) | hasta **+30 %** de esencias al rango 100, parejo con el rango | La fila de §0.4 de [Profesiones](../07-economia/profesiones.md) |
| Costo de encantar (`enchanting.enchant`) | ✨ 3 + 1 cada 10 niveles de la pieza; 🔮 1 desde el nivel 50; material 1 + 1 cada 50 niveles; 2 ⚡ y 12 de experiencia | Encantar lo mejor del juego gasta ~1,5 piezas raras del 100 y una épica: el sumidero crece con el nivel. Material de otros tres oficios (🔩 Fundición, 🧴 Destilación, 💠 Minero) |
| Valor de cada encantamiento (`enchanting.enchants`) | ⚔️ Filo (arma, manos) y ❤️ Vigor (pecho, cabeza, piernas): +1 % (rangos 1-25), +2 % (26-75), +3 % (76-100). 🛡️ Guarda (pies, joya): +1 de defensa (25-50), +2 (51-100) | Uno por pieza, la ranura decide. Con las 7 ranuras al rango 100: **+6 % de ataque, +9 % de vida y +4 de defensa**, algo así como dos beneficios de oficio (la Peletería da +4 % y +3 %; la Herrería, +3 de defensa) |
| Precio de las esencias (`items.yaml`) | ✨ 2 (el mercader paga 1 🥉), 🔮 6 (paga 3 🥉); 💱 Vender todo no las vende | Desencantar y vender nunca paga más que vender la pieza, ni con el beneficio al 100 (`tests/test_oficios_equipo.py`, pieza por pieza) |
| Puntaje de una pieza (`gear.score`) | ataque % + vida % + 2 × defensa | El que ya usaba la comparación ⬆️/⬇️; decide el aviso "⬆️ Tienes una pieza mejor" |
| Artesano de cabeza, manos, piernas y pies (`items.yaml`, 208 piezas) | Niveles 3, 5 y 8: el botín de su nivel y un bono chico; del 10 al 100: 🟣 épica, cada bono del botín × 1,1 (redondeado) y +1 % de ataque en cabeza, piernas y pies (+2 % desde el 60) o +1 de defensa en las manos. Precio: botín × 1,11 (5 y 8) y × 1,15 (10 a 100) | La curva del pecho de artesano (~10 % más que el botín y un bono), en chico |
| Sus recetas (`professions.yaml`, 208) | Los materiales del pecho de su tipo y nivel × su precio / el del pecho (~75 %), al menos 1 de cada uno, y siempre más valiosos que lo que paga el mercader por la pieza (también con la obra maestra); rangos 1, 25, 50 y 55 a 100 | Fabricar nunca fabrica monedas (D-113, D-116) |
| Obra maestra de esas ranuras (`masterwork.extra`) | cabeza, piernas y pies +1 % de ataque; manos +1 de defensa | La mitad del bono del pecho: son piezas chicas |

**Cómo se midió.** `tools/balance_report.py --scenarios=b,c --levels=10,50,100 --roles` (6 peleas por enemigo) con el contenido nuevo y con el de antes (`--content`). El escenario **b** (botín de su nivel) no cambia. El **c** (artesano donde lo hay + oficios al 100) ahora pone artesano en las 7 ranuras (mediana de vida al terminar, ataque / defensa / curación / soporte; antes → ahora):

| Escenario c | Nivel 10 | Nivel 50 | Nivel 100 |
|---|---|---|---|
| Vida al terminar | 76/75/84/76 → **77/76/85/77** | 70/81/79/74 → **72/83/80/76** | 70/82/82/73 → **72/83/83/75** |
| Rondas | 6,2/8,5/12,7/10,4 → **6,1/8,3/12,1/10,1** | 5,8/10,5/11,0/7,6 → **5,7/10,3/10,6/7,5** | 6,1/10,8/12,3/9,7 → **6,0/10,4/11,8/9,2** |

El artesano de las cuatro ranuras suma **+1 a +2 puntos** de vida al terminar y mata algo más rápido; el orden de los roles no cambia y todas ganan el 100 %. Los encantamientos no entran en el informe (son por pieza y opcionales); su tope (+6 % de ataque, +9 % de vida y +4 de defensa con todo encantado al rango 100) es del tamaño de dos beneficios de oficio. Si se los quiere medir, agregarlos al escenario c.

**Lo que queda por mirar:** si los encantadores encuentran equipo para desencantar (en la beta, contar cuántas piezas se desencantan y cuántas se venden); si la demanda de 💠 gemas y 🌸 flores de luna del artesano de las cuatro ranuras nuevas deja sin material a la Joyería y la Alquimia (subir `professions.rare_chance` o bajar las recetas); y si el aviso ⬆️ con su botón hace que nadie mire 🛡️ Equipo (eso está bien: es para eso).

### Octubre de 2026: los oficios del campamento, fase 2 (D-115, D-116)

**Por qué.** El dueño pidió muchos oficios que dependan unos de otros y mantengan el sistema (D-115), y beneficios que sean solo del campamento o del castillo (D-116). Entran los cuatro del lado del campamento de la fase 2 ([Red de oficios](../07-economia/red-de-oficios.md) §5; [Profesiones](../07-economia/profesiones.md) §0.4): 🎣 Pescador, 🍲 Cocina, 🗿 Cantería y 🏗️ Construcción. Son números **nuevos**, propuestos por Claude (`content/balance.yaml` → `camp_professions`; beneficios en `content/professions.yaml`; agua en `content/biomes.yaml`; comidas en `content/items.yaml`). Los únicos números de antes que se movieron son los **costos de las 4 mejoras del nivel 7 y 8** (con el mismo valor en crudo). No se tocó `hero.xp_formula` (P-77).

| Número | Antes | Ahora | Por qué |
|---|---|---|---|
| Zonas con agua (`biomes.yaml` → `water`) | — | pantano 1,0 · bosque 0,3 · pradera 0,3 | El pescado necesita agua: todo el pantano, y los ríos y lagunas de 3 de cada 10 zonas de bosque y de pradera. Con la semilla 12345, ~22 % de las zonas cerca del Claro |
| Peso del pescado (`camp_professions.fish.richness`) | — | 0,5 | Se suma a los recursos de tierra sin quitar ninguno; en el pantano es ~1 de cada 4 unidades de una vuelta (la hierba y la fibra rinden ~25 % menos ahí). Experiencia de Pescador: 1 por unidad, como todo recolector |
| Raciones del pescado (`items.yaml` → pescado.food) | — | 1 (la carne, 2) | Se junta más fácil que la carne (sale recolectando, sin pelear) |
| Platos de la 🍲 Cocina (`items.yaml` → `food`) | — | ×1,5 lo crudo en el rango 1, ×1,75 en el 25, ×2 en el 50, ×2,25 en el 75, ×2,5 en el 100 (3, 3, 10, 18, 27 y 45 raciones) | Cocinar vale la energía: el rango 1 suma 1 ración por ⚡; el 100, ~13 por ⚡. Nunca se venden (son `kind: food`): no fabrican monedas |
| 🧱 Sillar (receta `sillar`, `items.yaml`) | — | 3 piedras → 1 sillar, 1 ⚡, 6 de experiencia; precio 7 | Como el tablón: refinar no fabrica monedas (se vende a 3, lo que valen sus 3 piedras) |
| Costos del nivel 7 y 8 (`camp_upgrades.yaml`: enfermería, biblioteca, torres de arqueros, foso) | solo crudo | parte en 🧱 sillar y 🟫 tablón, mismo valor en crudo (460, 530, 560 y 600) | Que las mejoras grandes necesiten a la Cantería y al Aserradero. Cuestan además la energía de refinar (60 a 125 ⚡ entre todos). Lo crudo ya aportado de más cuenta como refinado |
| Beneficio del 🎣 Pescador (`pescador.perk.fish_food`) | — | +30 % de raciones del pescado crudo en la despensa, al rango 100 | Tabla de §0.4 de Profesiones |
| Beneficio de la 🍲 Cocina (`cocina.perk.cook_food`) | — | +30 % de raciones de lo cocinado, al rango 100 | Tabla de §0.4 |
| Beneficio de la 🗿 Cantería (`canteria.perk.stone_cost`) | — | −15 % de piedra y sillar en las obras, al rango 100 | Tabla de §0.4 (`camp_professions.stone_items`) |
| Beneficio de la 🏗️ Construcción (`construccion.perk`) | — | −20 % de materiales en las mejoras y −50 % al reparar, al rango 100 | Tabla de §0.4. Las monedas de las obras no bajan |
| Cómo suman los beneficios de campamento | — | rige **el mejor rango** entre los miembros de ahora (no se suman) | Simple y justo: un campamento grande no rinde más por tener diez cocineros. Decisión de Claude, provisional |
| Experiencia de 🏗️ Construcción (`camp_professions.build_xp_per_unit`) | — | 1 por material crudo aportado; un refinado, 3 | Quien junta y aporta todo lo de un día (150 a 300 unidades según su nivel) llega al rango 100 en ~1 a 1,5 años |
| Daño de las oleadas (`camp_professions.damage`) | — | −1 de 🛡️ Defensa si se defiende, −2 si se pierde; nunca más que lo construido; la Noche de prueba no daña | Que las defensas se gasten y haya trabajo para el Aserradero, la Cantería y la Construcción todas las semanas (red de oficios, regla 2: todo se gasta) |
| Reparar (`camp_professions.repair_per_point`) | — | 2 🟫 tablones y 2 🧱 sillares por punto (12 de lo crudo y 4 ⚡ de refinar) | Más barato que construir la defensa de nuevo (la Empalizada, 40 de lo crudo por 1 punto); la Construcción al 100 lo deja en la mitad |

**Cuenta rápida.**
- **Despensa:** un campamento de 10 miembros come 10 raciones por día. Un pescador dedicado en el pantano junta ~1 pescado por ⚡ (≈40 raciones al día); cocinadas en 🥫 conservas valen el doble. La comida deja de ser el freno para quien se organiza, y la despensa sigue comiendo todos los días (el sumidero).
- **Defensas:** con una oleada por semana, un campamento con defensas repara 1 o 2 puntos por semana: 4 a 8 refinados de cada uno (24 a 48 de lo crudo y 8 a 16 ⚡ de refinar), la mitad con un constructor de rango 100.

**Lo que queda por mirar:** si el pescado en el bosque y la pradera baja demasiado la madera y la hierba de esas zonas (bajar `fish.richness` o `water`); si las comidas grandes llenan la despensa tanto que el 🍖 Ahumadero y el 🥬 Huerto dejan de importar; si el daño de una oleada defendida (−1) se siente como castigo (se puede dejar en 0); y si "el mejor rango" debería sumar algo por un segundo especialista cuando haya especializaciones.

### Octubre de 2026: las 🎓 especializaciones de oficio (D-115, D-141)

**Por qué.** El dueño confirmó una especialización al rango 25 y otra al 75, nunca las tres (D-141), con recetas que solo ella hace, mejor calidad en su línea y más rendimiento, y cambiar pagando y empezando de cero ([Red de oficios](../07-economia/red-de-oficios.md) §3). El costo de cambiar sigue la recomendación de P-105 (monedas que suben con el rango). Números **nuevos** (nada movido), propuestos por Claude y a ajustar en la beta.

| Número | Valor | Por qué |
|---|---|---|
| Lugares (`specs.slots_at`) | rango 25 y 75 | D-141 |
| Dominio al 100 % (`specs.mastery_xp`) | 7.200 de experiencia de oficio ganada con la especialización (~1 mes dedicado, a ~240 por día); el efecto crece parejo desde 0 | "Empezar de cero" de verdad al cambiar, sin hacer que la primera tarde un mes en rendir del todo (a la semana ya da un cuarto) |
| Recetas exclusivas (`specs.recipe_mastery`) | con 25 % de dominio (~1 semana) y el rango de la receta | La recompensa llega pronto después de elegir |
| Cambiar (`specs.switch_cost`) | 100 🥉 + 20 🥉 por rango (25: 6 🥈; 50: 11 🥈; 75: 16 🥈; 100: 21 🥈) | P-105. Del orden de reiniciar los talentos (10 🥉 por nivel) y de unas 30-40 peleas de ese nivel: hace pensar, no castiga. Es un sumidero de monedas |
| Rendimiento (`yield`) | recolectores +20 % en su material; refinadores +15 % en su refinado (o +5 % y algo de su línea); remedios +20-25 %; 🔧 Herramientas +5 % en todo lo recolectado | El especialista junta y refina claramente más que quien hace de todo (red de oficios §1, regla 3). Refinar sigue sin fabricar monedas: lo que sale vale en el mercader lo mismo que lo que entra |
| Hallazgos (`find`) | 💠 Gemas y 🌸 Flores raras +8 % por vuelta; 🦴 Trofeos +3 % por unidad desollada; 🪙 Metales preciosos +3 % por vez | Más gemas y flores para las recetas altas, que las piden mucho desde la fase 2 |
| ✒️ Obra maestra (`masterwork`) | +5 % en su línea para los artesanos de equipo (Herrería y los demás pasan de 5 % a 10 % al rango 100; la Carpintería de 🏹 Arquería, de 15 % a 20 %); +2 % para algunos refinadores en su línea | "Mejor calidad en su línea" hasta que llegue la calidad (D-143). Con 20 %, vender todo lo fabricado rinde en promedio ~5 % sobre el valor de los materiales (antes, a lo sumo ~4 %): se acepta porque cuesta energía y el mercado lo pondrá en su precio |
| Efectos de combate (`perk`) | 🍷 Elixires: pociones +10 %; 🩹 Primeros auxilios: vendas y ungüentos +15 %; 🩺 Cirugía: curaciones +10 % (sanadores); ☠️ Venenos: +2 % de ataque; ✨ Armas y Armaduras: +1 punto al encantar | Chicos, del tamaño de medio beneficio de oficio (D-111). No entran en `tools/balance_report.py` (son opcionales y de uno solo); su tope es menor que el de un beneficio |
| Monedas (`coins`) | 💱 Comercio: +10 % en materiales, equipo o trueque, según la especialización; 🐾 Rastreador: +30 % de los campamentos enemigos | El comerciante gana su lugar con dinero (D-116). Con el beneficio del Comercio al 100 (+20 %), una venta de su línea paga hasta +30 %: la misma fuente de monedas que ya aceptó D-116, un poco más grande y solo en una clase de venta |
| Piezas exclusivas (`items.yaml`, 16 `espec_*`) | la pieza de artesano de su ranura, tipo y nivel (5 y 100) con cada bono × 1,05 (redondeado a puntos) y un punto propio; precio × 1,05; materiales de su receta de artesano + 1 (nivel 5) o + 1 gema y 1 flor de luna (nivel 100) | "El Armero hace las mejores placas". Siempre superan al artesano de su nivel y se venden por menos que sus materiales (`tests/test_especializaciones.py`) |
| Muebles exclusivos | 🛡️ Paveses de roble (rango 50): +1 de Defensa; 🛒 Carro de víveres (rango 25): los miembros comen 5 % menos | Como los de la Carpintería: 4 ⚡ y 24 de experiencia, uno de cada uno por campamento |

**Cómo se midió.** Las cuentas puras y los efectos en su línea con `tests/test_especializaciones.py` (rendimiento, hallazgos, obra maestra, curación, monedas, encantar, infiltrarse; solo en su línea y parejo con el dominio). El informe de clases (`tools/balance_report.py`) toma las piezas exclusivas en el escenario **c** (artesano donde lo hay) en los niveles 5 y 100: suman a lo sumo un 5 % en arma, pecho y joya, menos de lo que mueve un nivel de pieza.

**Lo que queda por mirar:** cuántos jugadores eligen cada especialización (si una nadie la toma, subir su efecto; si todos, bajarlo), cuántas veces se cambia (si nadie cambia, el costo es alto; si se cambia todos los días, bajo), cuánto material de más entra por día por especializaciones (meta: el especialista junta 15-20 % más, nunca el doble) y si las obras maestras se vuelven comunes en alguna línea.

### Octubre de 2026: las mazmorras para uno (D-164, D-165, D-170, D-171)

**Por qué.** El dueño pidió mazmorras con estructura fija que cambian cada día de facción, jefe, camino y botín (D-164), botín de otras clases para vender (D-165) y, para el que juega solo, mazmorras chicas de recompensa modesta y mazmorras profundas por pisos (D-170), con un mapa que muestra que hay algo sin decir qué (D-171). Ver [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) §0. Son números **nuevos**, propuestos por Claude (`content/balance.yaml` → `dungeons`; las familias, en `content/dungeons.yaml`). No se movió ningún número de antes; `hero.xp_formula` y `world.epoch` no se tocaron (D-118, D-64). El botín de las peleas sigue igual (70 % de tu tipo: P-111 sin decidir); solo el cofre y la bolsa de las mazmorras dan piezas de cualquier clase por igual.

| Número | Valor | Por qué |
|---|---|---|
| Entradas (`dungeons.stretch`, `second_chance`, `min_lejania`, `spacing`) | Tramos de 6 × 6 zonas con 1 entrada, o 2 con 50 %, desde Lejanía 2, nunca pegadas dentro del tramo | D-171: "1 o 2 mazmorras por tramo". En un mapa de 13 × 13 se ven unas 6 a 9 (con la semilla 12345, 24 en las 625 zonas a 12 del Claro: ~4 %) |
| Profundas (`deep_share`) | 1 de cada 4 entradas | Que la profunda sea algo que se busca, y la chica lo de todos los días |
| ❓ en el mapa (`hint_radius`) | A 2 zonas o menos de una zona que recuerdas | Lo que exploraste cerca te dice que hay algo; qué es lo sabes al pisarla o estudiarla desde al lado |
| Nivel (`level_bonus`) | Zona + 1 | Como los 👹 campamentos enemigos: algo más que cazar en la misma zona |
| Chica: estructura y energía (`small.rooms`, `fight_energy`) | 4 salas y el jefe; 2 ⚡ por pelea (10 ⚡ toda) | Estructura fija (D-164); 2 ⚡ como una presa o un asalto (D-108) |
| Jefe (`small.boss_hp_mult`, `boss_attack_mult`; igual en `deep`) | El más fuerte de la familia en ese nivel, vida × 1,8 y ataque × 1,2 | Como el jefe de un campamento enemigo: más difícil sin pedir grupo |
| Cofre de la chica (`small.chest`) | Monedas de 1,5 peleas comunes de su nivel (`coin_unit` 4 × (1 + 0,1 × (nivel − 1))), 1 a 3 materiales de la familia, 20 % de una pieza de su nivel de cualquier clase; sin experiencia | "Modesto" (D-170): el de un campamento enemigo da nivel × 25 🥉, 3 a 5 materiales, 50 % de equipo y experiencia. Una vez por mazmorra y día |
| Profunda: entrada y peleas (`deep.enter_energy`, `fight_energy`) | 2 ⚡ para entrar y 2 ⚡ por pelea | La entrada hace que una bajada corta rinda algo menos que cazar |
| Profunda: pisos (`two_fights_chance`, `level_per_floor`, `hp_per_floor`, `attack_per_floor`, `boss_every`) | Piso 1: 1 pelea; desde el 2, 1 o 2 (35 %); +1 nivel, +5 % de vida y +3 % de ataque por piso; jefe cada 5 | Que cada piso se sienta más duro y que, sin curarse, la bajada termine en algún lado |
| Bolsa (`deep.pot`) | Por piso: media pelea de monedas y 1 material; en los pisos de jefe, 30 % de una pieza de cualquier clase | El premio por bajar más, que solo se cobra entero si sales a tiempo |
| Perder abajo (`deep.defeat_keep`) | La mitad de la bolsa (huir, igual, pero sin quedar malherido) | El riesgo de seguir bajando; lo de cada pelea es tuyo igual |
| Lista del día (`deep.top_listed`) | Los 3 más hondos de cada mazmorra profunda | Una razón social para bajar un piso más |

**Experiencia y monedas por ⚡ frente a 🏹 Cazar** (promedio de las 14 familias frente al de los 8 biomas con peligro; cazar: el enemigo del nivel de la zona, o + 1 con 30 %; la profunda: 5 pisos con ~1,35 peleas por piso desde el 2 y la entrada):

| Zona | Cazar | 🕳️ Chica | 🌀 Profunda, 5 pisos |
|---|---|---|---|
| 3 | 26 · 3,3 🥉 | 28 (×1,07) · 4,0 🥉 (×1,23) | 30 (×1,16) |
| 6 | 36 · 4,1 🥉 | 38 (×1,07) · 5,2 🥉 (×1,26) | 40 (×1,11) |
| 10 | 52 · 6,0 🥉 | 54 (×1,04) · 6,7 🥉 (×1,12) | 54 (×1,03) |
| 20 | 85 · 10,3 🥉 | 85 (×0,99) · 10,4 🥉 (×1,01) | 79 (×0,93) |
| 40 | 152 · 19,6 🥉 | 155 (×1,02) · 21,1 🥉 (×1,08) | 140 (×0,92) |
| 60 | 222 · 29,8 🥉 | 228 (×1,03) · 32,3 🥉 (×1,09) | 204 (×0,92) |
| 90 | 327 · 46,4 🥉 | 337 (×1,03) · 52,2 🥉 (×1,13) | 297 (×0,91) |

La chica queda **a la par de cazar en experiencia** (×0,99 a ×1,07: el nivel + 1, sin experiencia extra en el cofre) y un poco arriba en monedas (×1,01 a ×1,26), más 1 a 3 materiales y 20 % de una pieza; el viaje hasta la entrada y las pociones comen la diferencia. La profunda de 5 pisos rinde algo menos por ⚡ (la entrada cuesta) y sube a medida que se baja (el nivel crece 1 por piso, como cazar en una zona más lejana, pero sin viajar y con los enemigos más duros): D-108 se mantiene.

**Medido con el motor** (`tools/balance_report.py`: `kit_for` "b" —puntos y botín de su nivel— y `fight` con juego atento; el héroe es del nivel de la zona y la mazmorra del nivel + 1; 8 especializaciones, 2 por rol; las 14 familias):

| Zona | Gana al jefe de la chica (vida llena) | Pisos de la profunda sin curarse (cinturón de 3 pociones y 2 vendas, y 3 + 3 de repuesto en la mochila) |
|---|---|---|
| 3 | 98 % (93 % la peor) | 2,9 en promedio (1 a 6) |
| 10 | 100 % | 3,4 (2 a 9) |
| 30 | 79 % (45 % el sacerdote y el paladín sagrado) | 3,4 (1 a 10) |
| 60 | 97 % (79 % la peor) | 7,7 (1 a 26; las defensas, 11 a 17) |
| 90 | 94 % (62 % la peor) | 9,7 (1 a 37; las defensas, 14 a 21) |

El jefe de la chica se gana como el de un 👹 campamento enemigo (85-97 %), con un bache en la zona 30 para dos especializaciones de curación (el mismo bache de esos niveles en la pasada de D-110). En la profunda, el que juega su nivel baja 3 o 4 pisos y las defensas, que aguantan sin curarse, bajan mucho más en los niveles altos: el récord y la lista 🏆 lo premian.

**Lo que queda por mirar:** si 1 o 2 entradas por tramo de 6 × 6 son muchas o pocas en la beta; si el cofre de la chica (1,5 peleas de monedas, 20 % de equipo) se siente demasiado modesto; si la profunda debería tener un tope de nivel por piso para que las defensas no bajen 30 pisos en los niveles altos; si huir abajo debería costar menos que caer; y cuánto equipo de otras clases entra por día (D-165) cuando exista el mercado (D-137).

### Octubre de 2026: 🔭 Reconocer y 🥷 Sigilo del Explorador (D-172)

**Por qué.** El dueño pidió que el 🧭 Explorador aprenda sigilo y reconocimiento: saber qué hay en un lugar antes de llegar, con experiencia y recompensas propias (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.14, "🔭 Reconocer y 🥷 Sigilo"). Son números **nuevos**, propuestos por Claude (`content/balance.yaml` → `recon` y `explorer.ranks.recon`, `recon_far`, `recon_wide`, `stealth_max`; el sigilo, en `content/professions.yaml` → explorador.perk y explorador_infiltrado). No se movió ningún número de antes; `hero.xp_formula` y `world.epoch` no se tocaron (D-118, D-64).

| Número | Valor | Por qué |
|---|---|---|
| Alcance de 🔭 (`recon.range` con `explorer.ranks.recon`, `recon_far`, `recon_wide`) | 1 zona a la redonda al rango 10, 2 al 30, 3 al 50; nunca tu propia zona | Usa los umbrales que ya existían (10, 30, 50), así el Explorador no suma escalones nuevos; el alcance nunca pasa de lo que ya ve del mapa (la vista de campamentos es 1, 3 y todo el mapa) |
| Energía (`recon.energy`) | 2 ⚡ | Como una pelea de asalto o una presa: algo que se piensa, no que se repite sin mirar |
| Experiencia de Explorador (`recon.explorer_xp`) | 12 | 6 por ⚡, lo mismo que explorar (5 por vuelta y 6 al completar una zona) y algo más que infiltrarse (15 por 3 ⚡): reconocer no acelera el oficio, lo acompaña |
| Experiencia de héroe (`recon.hero_xp`) | 6 | La de 2 vueltas de explorar (`explore.xp_per_step` × 2): el ⚡ no rinde menos que explorando sin peleas (D-108) |
| Monedas (`recon.coins_per_level`) | nivel del lugar × 2 🥉 (nivel 4: 8 🥉; nivel 40: 80 🥉) | ~1 × nivel por ⚡; explorar da ~0,7 × nivel por ⚡ en monedas (20 % de las vueltas, nivel × 2 a 5) más hallazgos y el botín de sus peleas. Sin objeto que se vende (P-120 sigue abierta) |
| Uno por lugar y día | — | Con la semilla de prueba hay, en promedio, 0,5 lugares para reconocer a 1 zona, 1,7 a 2 y 3,2 a 3 (todas las entradas y campamentos, antes de mirar el mapa del héroe): unos 2 a 8 ⚡ por día, un rato y no un camino entero |
| Lugares listados (`recon.listed`) | 6, con 3 botones | La pantalla corta (D-86) y el tope de 4 botones |
| Sigilo del oficio (`perk: {stealth: 0.25}`) | 0,25 % por rango: 2,5 % al 10, 12,5 % al 50, 25 % al 100 | Parejo con el rango como todo beneficio (D-111); 1 de cada 4 peleas al azar al rango 100 |
| Sigilo de la 🕵️ Infiltrado (efecto `perk` `stealth`) | +10 puntos con todo el dominio | La especialización de "moverse como una sombra" (D-141); con el rango 100, 35 % |
| Tope (`explorer.stealth_max`) | 50 % | Que ningún beneficio futuro deje explorar sin peleas |

**Cuánto cambia el sigilo.** Explorar da una pelea al azar en el 45 % de las vueltas (`explore.encounter`). Con ✋ Manual, cada pelea corta el lote: sin sigilo, un lote dura en promedio ~2,2 vueltas antes de cortarse; con 12,5 % (rango 50), ~2,5; con 25 % (rango 100), ~3,0; con la Infiltrado (35 %), ~3,4. La vuelta evitada no da hallazgo ni monedas (sí la exploración y la experiencia de explorar). Al llegar de un viaje, la emboscada sale con la probabilidad del bioma (25 % a 50 %); el sigilo evita 1 de cada 4 al rango 100. Con ⚔️ Automática el sigilo no se usa: el jugador eligió pelear, y la experiencia por ⚡ de esos lotes queda igual que antes (D-108).

**Lo que queda por mirar:** si los jugadores reconocen tanto que dejan de explorar (medir ⚡ por día en cada cosa); si 2 ⚡ es caro para saber la familia de una mazmorra (si nadie reconoce, bajar a 1); si recolectar con ✋ Manual también debería usar el sigilo; si el sigilo debería poder apagarse en ⚙️ Opciones para quien quiere todas las peleas sin pasar a ⚔️ Automática; y, si se decide P-120, si el reconocimiento debería dar un 📜 informe que se vende en vez de monedas.

### Octubre de 2026: los recursos de cada terreno y los nodos de recursos (D-180, D-181, D-183, D-184)

**Por qué.** El dueño pidió (1-oct-2026) que cada terreno tenga un catálogo de 10 a 15 recursos y que cada zona traiga solo una parte (D-180), y nodos de recursos con un símbolo genérico que se descubren al llegar (D-181). Se aplicó lo recomendado en E-123 y E-124 (D-183, D-184, provisionales; ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.12.2 y §1.16). Son números **nuevos**, propuestos por Claude. Se movió uno de antes: `exploration.reveal_at`. `hero.xp_formula` y `world.epoch` no se tocaron (D-118, D-64).

| Número | Antes | Ahora | Por qué |
|---|---|---|---|
| Propios por zona (`resources.terrain.add`) | — | 2 o 3 | D-180: "4 o 6 de los 15"; con los 1 a 3 de base quedan 4 a 6 |
| Recursos de tierra por zona (`resources.terrain.total`) | 1 a 3 | 4 a 6 (el pescado aparte) | Con 1 de base suma 3, nunca pasa de 6: la pantalla de 📍 Zona sigue corta |
| Riqueza de los propios (`resources.terrain.richness`) | — | 0,3 a 1,0 | La misma escala que los de base (el más fuerte vale 1,0) |
| Catálogo por terreno (`biomes.yaml` own) | 2 o 3 recursos | 10 (sus 2 o 3 de base + 7 u 8 propios) | El piso del pedido (10 a 15): deja lugar para lo que traigan el 🌾 Agricultor y el 🐑 Ganadero |
| Precio de los 21 materiales nuevos | — | 2 a 5 🥉 (el mercader paga la mitad) | Cerca de los de base (2 a 6): recolectar rinde lo mismo en monedas por ⚡ |
| Descubrir recursos (`exploration.reveal_at`) | 1, 50, 100 % (3 recursos) | 1, 20, 40, 60, 80, 100 % | Uno por umbral hasta 6; para cada porcentaje se conoce lo mismo o más que antes (los de base van primero) |
| Nodos por tramo (`nodes.count`, `stretch`) | — | 2 o 3 por tramo de 6 × 6 | D-171: "2 o 3 iconos de nodos por tramo"; ~7 % de las zonas (115 de 1.680 en la semilla de prueba) |
| Rinde (`nodes.yield_mult`) | — | ×2 su recurso | E-124: "su recurso rinde el doble" |
| Se agota (`nodes.stock_mult`) | — | la mitad | E-124: "se agota más despacio": con ×2 de rendimiento, un nodo da 4 veces más de su recurso antes de agotarse |
| Raro (`nodes.rare_chance`) | — | 5 % por vuelta con algo recolectado | Como el raro de los oficios al rango 10 (`professions.rare_chance`), pero sin pedir rango: 1 💠 o 🌸 cada ~20 vueltas en un nodo |
| Recurso del nodo (`nodes.own_share`) | — | 6 de cada 10, un propio del terreno | Que los nodos lleven a buscar lo propio de cada terreno; los demás, el más fuerte de la zona |
| Pista en el mapa (`nodes.hint_radius`) | — | 2 zonas | Igual que las cuevas (`dungeons.hint_radius`) |

**Cuánto cambia recolectar.** Cada vuelta saca las **mismas unidades** que antes (`gather.amount`), repartidas entre más recursos: no se multiplican. Lo que sí cambia es cuánto sale de los 6 de base: en promedio, una vuelta da **53 %** de lo que daba de ellos (63 % en las zonas con 3 de base, 54 % con 2 y 34 % con 1), y el resto son materiales del terreno, que se venden a precios parecidos o se usan en las 22 recetas nuevas. Un nodo duplica solo su recurso (y con eso la experiencia de oficio por unidad de ese recurso; la de héroe sigue siendo por vuelta). Las unidades de más y el raro usan su propio sorteo.

**Lo que queda por mirar:** si fundar, agrandar y las mejoras del campamento quedan lentas porque llega menos madera y piedra por vuelta (si pasa, bajar `resources.terrain.richness` a 0,3-0,7 o sumar menos propios en las zonas con 1 de base); si los nodos concentran a todos en pocos lugares (el agotamiento es para todos); si entran demasiadas 💠 gemas y 🌸 flores de luna por los nodos frente a los oficios; y si 10 por terreno alcanza o conviene subir a 12-15 cuando lleguen el Agricultor y el Ganadero.

### Octubre de 2026: el camino guiado (D-190, D-193, provisional)

**Por qué.** El camino guiado reemplazó al tutorial de pistas (0.29). Los números los propuso Claude, parecidos a los del tutorial viejo por paso; se ajustan en la beta.

| Qué | Antes | Ahora | Por qué |
|---|---|---|---|
| Premio por paso (`tutorial.reward_*` → `guide.reward_gold`, `guide.reward_xp`) | 5 🥉 y 20 de experiencia × 7 pasos (35 🥉, 140) | 5 🥉 y 20 de experiencia × 10 pasos con premio (50 🥉, 200) | Lo mismo por paso; el camino tiene más pasos. 200 de experiencia es el nivel 2 (pide 120) y algo más: no es un atajo (el nivel 3 pide 612) |
| Veterano (`guide.veteran_level`) | — | nivel 5 | E-133: quien llegó al nivel 5 ya conoce lo básico; se salta el camino sin premio |
| Movimientos antes de "buscar lugar" (`guide.found_moves`) | — | 2 zonas pisadas fuera del Claro | D-190: "uno o dos movimientos" después de salir; además el lugar tiene que servir (Lejanía 2 o más, `camps.min_lejania`) |
| Aviso de energía baja (`guide.energy_low`) | — | 10 ⚡ | Una quinta parte del máximo (50): todavía alcanza para un lote chico |
| Aviso de ⚙️ Opciones (`guide.options_kills`) | — | 3 peleas ganadas | Después del paso 🏹 Cazar, cuando ya peleó un poco |

**Lo que queda por mirar:** en qué paso se queda la gente y cuánto tarda en terminar el camino básico (mapa de impacto, C-29). Si moverse pasa a no gastar energía (E-135), el texto cambia solo.

### Octubre de 2026: 1 minuto por cuadro y toda la energía de entrada (D-196, D-197, confirmadas; 0.29.1)

**Por qué.** El dueño decidió el 2-oct-2026: "moverse no cuesta energía; cuesta tiempo: 1 minuto real por cuadro" y "para empezar una acción, el jugador debe tener de entrada toda la energía que esa acción requiere".

| Qué | Antes | Ahora | Por qué |
|---|---|---|---|
| Minutos por zona (`travel.first_minutes`) | 2 las 2 primeras zonas desde el Claro o tu campamento (D-78) | 1, en cualquier zona | D-197: 10 cuadros = 10 minutos |
| Aumento por lejanía (`travel.steps_per_minute`) | 2 (cada 2 zonas, 1 minuto más: 2, 2, 3, 3, 4…) | 0 (sin aumento) | D-197. La fórmula vieja vuelve si se sube a más de 0 |
| Tope por zona (`travel.max_minutes`) | 20 | 20 (sin efecto con 0) | Se deja por si vuelve la regla vieja |
| Pasos de 🔗 Moverte (`travel.walk_max`) | — (no existía) | 50 | D-244 (0.33): "hasta 50 sin problema". Moverse no gasta energía, así que 50 pasos son unos 50 minutos de viaje |
| Aprender un oficio (`professions.learn_price`) | — (se aprendía haciéndolo, D-57) | 🥉20 por oficio; gratis si ya lo practicabas | D-257 (0.33): la regla es del dueño; el número, de Claude (P-231) |
| Posada: rapidez (`inn.speed`) y mínimo (`inn.min_minutes`) | 5 minutos fijos (`inn.minutes`) | 4 veces más rápido que sola (de 0 a llena en 60 min), mínimo 5 min | D-259 (0.33): "no te lo puede llenar en 5 minutos". El 🛏️ Refugio del campamento usa la misma cuenta |
| Peleas automáticas (`auto_fight.enabled`) | sí (D-114) | no | D-258 (0.33): el dueño las quitó por ahora, con las pociones automáticas |
| Largo del 💬 Feedback (`feedback.max_chars`) | — | 1.000 caracteres | D-258 (0.33) |
| 🕳️ Mazmorra chica | Se entraba con 2 ⚡ y se cobraba pelea por pelea | Pide de entrada la energía de todas las peleas que faltan hoy (10 ⚡ al empezar); se cobra igual, pelea por pelea | D-196: nadie queda a medias |
| 🌀 Mazmorra profunda | Cada pelea pedía 2 ⚡ (4 la primera, con la entrada) | Cada piso pide de entrada todas sus peleas (4 si tiene 2 peleas; 4 el piso 1 con la entrada) | D-196: el piso es la acción |

**Cuánto cambia.** Un viaje de 10 zonas desde el Claro tardaba 2 + 2 + 3 + 3 + 4 + 4 + 5 + 5 + 6 + 6 = 40 minutos; ahora tarda 10. Lo lejano queda mucho más cerca: el valor de fundar un campamento lejos para viajar menos baja (ya no reinicia la cuenta), pero sigue el territorio, los recursos y la seguridad. La experiencia y el botín por ⚡ no cambian: la energía de las mazmorras es la misma, solo se pide antes.

**Lo que queda por mirar:** si con viajes tan cortos la gente se junta en pocas zonas lejanas ricas (el agotamiento es para todos); si hace falta que las monturas o mejoras lo aceleren o, al revés, que el viaje largo cueste algo (E-161, E-162); el costo de energía por tamaño de nodo cuando existan los tamaños (E-165).


### Octubre de 2026: el 🗺️ Mapa gris por etapas (D-212, D-220, confirmadas; 0.30)

**Por qué.** El dueño pidió el 4-oct-2026: "regreses a los puntos grises todo el mapa. Y cuando lo investigas al 50 %, se te va a desbloquear el color, el tipo y la información", de "diferentes formas o maneras" para que se vea que avanzas poco a poco. Los porcentajes de las etapas los eligió Claude (a confirmar en E-194).

| Qué | Antes | Ahora | Por qué |
|---|---|---|---|
| Desde qué % se ve el color de una zona (`map_view.fog.color_at`) | 0 (todo el tablero a color desde la 0.26.2, D-186) | 50 | D-212 y D-220: "cuando lo investigas al 50 %" |
| ▫️ sin investigar (`map_view.fog.stages`, `unknown`) | — | desde 0 % | Los puntos grises de antes de la 0.26.1 |
| ◽ con rastros (`traces`) | — | desde 1 % | El mismo % en que se conoce el primer recurso (`exploration.reveal_at`): lo que ya encontraste se nota en el mapa |
| ◻️ reconocida (`scouted`, con aviso) | — | desde 25 % | La mitad del camino al color; con 🔎 Explorar (15 a 30 % por vuelta, `exploration.per_step`) suele llegar en la primera o la segunda vuelta |

**Cuánto cambia.** Nada del juego cambia de números: el porcentaje de exploración, lo que da cada vuelta y lo que se descubre al 1, 20, 40, 60, 80 y 100 % siguen iguales. Cambia lo que ves: para ver a color una zona hay que darle unas 2 o 3 vueltas de 🔎 Explorar (de 15 a 30 % cada una, `exploration.per_step`); en la zona de un 👹 campamento enemigo, 5 veces 🕵️ Infiltrarse del 🧭 Explorador (`enemy_camps.infiltrate.explore_points`, 10). Nadie pierde nada: lo que estaba al 50 % o más quedó a color.

**Lo que queda por mirar:** si con 3 etapas grises alcanza para "ver que avanzas" o hace falta otra (por ejemplo, el nombre del terreno al 25 %); si el 50 % se siente lento para quien explora poco; y si los jugadores confunden el ◻️ de reconocida con el ⬜ de la montaña (si pasa, se cambia la marca en `map_view.fog.stages` sin tocar nada más).

### Octubre de 2026 (8-oct): el parche de clases 0.31 (D-225 a D-232)

**Por qué.** El dueño reemplazó las 15 clases por 6 clases con 2 roles y la misma cadena para todas ([Combate en cadena](../04-combate/combate-en-cadena.md)). Los números del parche son la estructura (energía 5 y +2, costos 0/2/3/6, premio 10/25/50 %, gastador sin combo 85 %). La potencia de cada botón y el esqueleto de cada rol los midió Claude con el simulador. Es provisional (D-231) y se ajusta en la beta.

**Objetivos (los mismos de antes):**
- Contra cada enemigo de nivel 1 a 3: 90 % o más (curación: 85 %).
- Contra el Guardián al nivel 6: entre 45 y 90 %.
- A los niveles 50 y 75 (tests/test_balance_d110.py):
  - todos ganan el 85 % o más;
  - el tanque termina con más vida que el DPS;
  - el DPS es el que mata más rápido y la curación la más lenta;
  - la curación es la que más vida deja.
- Regla madre (D-232): las clases de un mismo rol comparten esqueleto. La diferencia dentro del rol no debería pasar de unos 15 puntos contra el Guardián.

**El esqueleto de cada rol** (`content/classes.yaml`, base y por nivel):

| Rol | Vida | Ataque | Armadura | Iniciativa | Por nivel |
|---|---|---|---|---|---|
| Tanque | 135 | 10,5 | 20 % | 9 | +16 vida, +1,5 ataque |
| Sanador | 110 | 9,8 | 10 % | 10 | +12 vida, +1,4 ataque |
| DPS | 160 | 13,5 | 10 % | 11 | +12 vida, +1,7 ataque |
| Soporte | 165 | 12,5 | 12 % | 11 | +14 vida, +1,5 ataque |

**Los botones.** Potencia × ataque; las curaciones se miden en parte de la vida máxima.

| Rol | Básico | Constructor | Preparador | Gastador |
|---|---|---|---|---|
| Tanque | 0,9 | 1,3 | Aguante o esquiva 35 % por 2 turnos | 1,0 (Druida: 0,6 + 0,06 por esquiva), y aguante o esquiva 40 % por 3 turnos |
| Sanador | Sacerdote 1,0 · Chamán 0,65 | Cura 15 % (Sacerdote: 10 % + 5 % el turno siguiente; Chamán: 3 × 5 %) | Sacerdote: escudo del 15 % · Chamán: golpe 1,35 y +25 % a la próxima curación grande | Sacerdote: cura 32 % (con premio) · Chamán: cura 36 % (sin premio, D-227) |
| DPS | 0,7 | 1,0 | Exponer 20 % por 3 turnos, sangrado o quemadura 0,3 por turno, sombra 0,3 y +10 %, o golpe 0,7 que carga +30 % | 1,9, más lo propio de cada clase (Ejecutar ×1,6 con el enemigo bajo el 35 %, consumir el daño en el tiempo, +0,25 por turno de sombra, ×1,25 con tu marca) |
| Soporte | 1,0 | 1,3 (alarga lo activo, hasta 3 turnos) | Cazador: potenciar 30 % · Mago: exponer 20 % (2 turnos) | Golpe 1,0, más Cazador: potenciar 40 % por 3 turnos · Mago: exponer 20 % y debilitar 5 % por 3 turnos, e interrumpir |

**Resultado** (`tools/sim.py`):
- Contra los enemigos de nivel 1 a 3, todas ganan el 100 %.
  - Rondas: DPS de 3,8 a 4,4; tanques de 7,7 a 7,9; sanadores de 8 a 8,6; soportes de 4,6 a 5,4.
  - Vida que les queda: de 66 a 81 %.
- Contra el Guardián al nivel 6 (80 peleas):

| Rol | Resultado |
|---|---|
| Tanques | 84 y 90 % |
| Sanadores | 85 y 90 % |
| DPS | Guerrero 82, Druida 80, Sacerdote 82, Chamán 74, Cazador 68, Mago 80 % |
| Soportes | Cazador 74, Mago 89 % |

**Lo que queda por mirar:**
- El Cazador DPS (68 %) y el soporte del Cazador (74 %) quedan algo por debajo de su pareja.
- Los avisos de los enemigos todavía dicen "se puede bloquear o esquivar". En las clases nuevas eso se contesta con 🛡️ Defenderse, el aguante o la esquiva del tanque, o la Ruptura del Mago.
- El nivel todavía da vida y ataque, hasta la reforma de estadísticas del equipo (D-232).

### Octubre de 2026 (9-oct): el Paladín en lugar del Chamán (0.32, D-233 y D-234)

**Por qué.** El dueño cambió el Chamán por el Paladín para tener dos clases por armadura ([Combate en cadena](../04-combate/combate-en-cadena.md) §11).

**Qué se movió:** ningún número. El Paladín · Sanador y el Paladín · DPS usan los botones, la vida, el ataque, la armadura y la iniciativa del Chamán; solo cambian los nombres y la escuela (sagrado). La armadura por grupo del Paladín es placa (`gear.armor_by_group`), igual que antes; el Chamán sigue en cuero, pero ya no se juega.

**Resultado** (`tools/sim.py`): contra el Guardián al nivel 6 (80 peleas), Paladín · Sanador 90 % y Paladín · DPS 74 %, los mismos números del Chamán; contra cada enemigo de nivel 1 a 3, el 100 % (sanador: 8 rondas y 66 % de vida al final; DPS: 3,9 rondas y 81 %).

### Octubre de 2026 (18-oct): viajes más seguros y monstruos de tu nivel (0.34, D-266, confirmada)

**Por qué.** El dueño: "no siempre que te muevas vas a pelear, porque vas a morir muchas veces… los mobs pueden ser de tu nivel, un poquito más o menos; cuando ya estamos hablando de una dungeon, sí es diferente".

**Qué se movió** (`content/balance.yaml`):

| Número | Antes | Ahora |
|---|---|---|
| `explore.arrival_encounter_scale` | 1,0 (pelea al llegar: 25 a 55 % por zona) | 0,25 (6 a 14 %) |
| `wild_level.below` / `above` (nuevo) | el nivel de los monstruos era el de la zona (+1 con 30 %) | el del héroe, de 1 menos a 2 más |
| `places.camps_listed` (nuevo) | — | 5 campamentos de jugadores en 📒 Lugares (D-267) |
| `professions.recommend_by_armor` (nuevo) | — | placas → Herrería, cuero → Peletería, tela → Sastrería (D-271) |

**Qué cambia al jugar.** Un viaje de 10 zonas por pradera trae pelea la mitad de las veces (antes el 94 %). Ir lejos ya no castiga a un jugador nuevo (resuelve P-203): el monstruo sale de su nivel, y la experiencia y el botín de pelear siguen al nivel del monstruo, así que tampoco hay premio extra por ir lejos. Los recursos raros y la experiencia de recolectar siguen subiendo con la lejanía. **A medir en la beta** con el informe diario: muertes por viaje y peleas por hora.

### Octubre de 2026 (18-oct): cambio de clase y recolección que se aprende (0.35, D-270 y D-272, confirmadas)

| Número | Antes | Ahora |
|---|---|---|
| `class_change.prices` (nuevo) | la clase no se cambiaba | 0, 100, 1.000, 3.000 y 5.000 🥉 (gratis, 🥈1, 🥈10, 🥈30 y 🥈50 para siempre) |
| `learn: auto` en `content/professions.yaml` | Leñador, Minero, Herbolario, Pescador y Explorador | solo el Explorador (los 4 de recolección llevan `grandfather: true`) |

**Qué cambia al jugar.** Un jugador nuevo recolecta solo los recursos base hasta aprender el oficio (🥉20): sin la unidad de más (rango × `rank_yield`), sin hallazgos raros (gemas desde el Minero 10) y sin experiencia. Ojo: la Joyería empieza pidiendo una 💠 gema, que sin el Minero sale solo de nodos (P-234). Quien ya recolectaba no pierde nada.

### Octubre de 2026 (18-oct): el gremio desde el inicio y las obras con tiempo (0.36; D-265, D-269 confirmadas; D-274 y D-276 provisionales)

**Por qué.** El dueño: "hay que empezar a crear los grupos desde el primer momento… entre más miembros haya dentro de la zona, más rápido se construye… y así funciona para todas las cosas". Y para la fogata: "un botón de jugadores… los que estuvieron en el último minuto… una cantidad máxima de 20 jugadores". Los números marcados "dueño" los dijo él; el resto los propuso Claude.

**Números nuevos** (`content/balance.yaml`):

| Número | Valor | De quién y por qué |
|---|---|---|
| `gremio.found_coins` | 🥉20 | Dueño: crear un gremio |
| `gremio.members_before_camp` | 5 | Dueño: los que caben antes del campamento |
| `gremio.found_min_members` | 2 | Dueño: miembros presentes para fundar |
| `gremio.found_minutes` | 60 | Dueño: fundar tarda 1 h con 2; con 4, 30 min (tiempo = 60 × 2 ÷ presentes) |
| `gremio.found_floor_minutes` | 10 | Dueño: nunca menos de 10 min |
| `gremio.message_max_chars` / `messages_kept` / `list_shown` | 200 / 5 / 8 | Claude: mensajes cortos para el teléfono; los últimos 5 en la pantalla; 8 gremios por lista |
| `works.minutes_per_level` / `members_ref` / `floor_minutes` | 60 / 2 / 10 | Claude sobre la regla del dueño (D-274.4): cada obra, 1 h por su nivel con 2 miembros en el territorio; con 1, el doble; nunca menos de 10 min |
| `presence.bonfire_seconds` | 60 | Dueño: 👥 Jugadores lista a los del último minuto |
| `bonfire.cap` | 20 | Dueño: el tope de cada fogata (en la 0.36 solo se muestra "N/20"; el reparto, en la 0.37) |

**Qué se movió:**

| Número | Antes | Ahora | Por qué |
|---|---|---|---|
| `guild.levels[0].capacity` (gremio del campamento, nivel 1) | 4 | 5 | Al fundar, el gremio de 5 pasa a ser el del campamento: con 4, uno quedaba afuera |

**Cuenta rápida.** Un gremio de 2 que junta el fondo (🪵 20 y 🪨 10, menos de una hora de recolectar entre los dos) y se encuentra en el lugar funda en 1 hora; con los 5, en 24 min. Una obra de nivel 1 tarda 1 h con 2 en el territorio y una de nivel 8 (foso, torres) 8 h con 2, o 3 h 12 min con 5: el castillo (15 mejoras) pide horas de estar juntos, no solo materiales. Con nadie en el territorio, la obra espera: no hay construcción "sola".

**Lo que queda por mirar:** si 60 min por nivel hace muy lentas las obras grandes para campamentos chicos; si la fundación con 1 solo presente debería pausarse (hoy avanza al doble de tiempo); cuántas obras quedan en pausa más de un día; cuántos invitados entran al campamento recién fundado.

### Octubre de 2026 (18-oct): las 9 hogueras y la Lejanía desde la más cercana (0.37, D-265 y D-277, confirmadas)

| Número | Antes | Ahora |
|---|---|---|
| `bonfire.spacing` (nuevo) | — | 12: una hoguera cada 12 zonas (D-224, D-265) |
| `bonfire.ring` (nuevo) | — | 1: las 8 de alrededor del Claro (9 en total) |
| `bonfire.cap` | 20, solo se mostraba | 20: llena, los nuevos nacen en la siguiente y los que llegan siguen hasta la más cercana con lugar |
| Lejanía de una zona (`mapgen.lejania`) | distancia al Claro | distancia a la hoguera más cercana (D-277) |

**Qué cambia al jugar.** Alrededor de cada hoguera nueva la tierra vuelve a ser de nivel bajo: una zona a 11 del Claro hacia el este pasó de Lejanía 11 a Lejanía 1. Lo más lejano también baja (una zona a 30 zonas del Claro queda a 18 de la hoguera más cercana): el anillo de recursos, el nivel de las mazmorras y de los campamentos enemigos bajan en todo el mapa de afuera. Los monstruos de afuera no cambian: ya salían del nivel del héroe (D-266).

**Lo que queda por mirar:** si con la Lejanía desde la más cercana el mapa de afuera queda demasiado fácil (si hace falta, que más allá del anillo de hogueras se cuente desde el Claro); cuántos jugadores nacen fuera del Claro y si las hogueras nuevas se sienten vacías.

### Octubre de 2026 (18-oct): lo que sabe el gremio (0.38, D-282, confirmada)

| Número | Antes | Ahora |
|---|---|---|
| `gremio.zones_shown` (nuevo) | — | 8: cuántas zonas lista 🗺️ Zonas del gremio de una vez (Claude) |

**Qué cambia al jugar.** Un gremio que se reparte las zonas conoce el mapa mucho más rápido: 5 miembros que exploran cada uno su parte conocen 5 veces más zonas que uno solo, y fundar ya no pide que el líder explore de nuevo la zona elegida. La experiencia no cambia: cada uno gana la suya explorando.

**Lo que queda por mirar:** si conocer el mapa entre todos hace demasiado fácil encontrar los nodos y recursos raros; cuántos jugadores usan 🗺️ Zonas del gremio.

### Octubre de 2026 (20-oct): ⏫ Siguiente nivel y 🗺️ Agrandar territorio (0.41, D-304)

| Número | Antes | Ahora |
|---|---|---|
| `camps.grow_cost_per_level` | 🪵15 🪨10 🌿5 × el nivel; cada vez sumaba 1 nivel y 1 zona | el mismo número × las zonas que ya tiene; suma solo 1 zona (para un campamento de antes, el mismo precio: su nivel era igual a sus zonas) |
| `camps.zones_by_stage` (nuevo) | — sin tope (1 zona por nivel) | campamento 3 · aldea 5 · pueblo 9 · ciudad 15 · castillo 25 (la tabla de E-218, confirmada por el dueño) |
| `camps.level_up` (nuevo) | — subir era agrandar | las obras construidas que pide cada nivel: 2 🔥 Fogón y 🪵 Empalizada · 3 🗼 Torre de vigía y ⛲ Pozo · 4 Refugio, Granero y Trampas · 5 Ahumadero, Perrera y Cabañas · 6 Muralla y Huerto · 7 Braseros · 8 Enfermería y Biblioteca · 9 Torres de arqueros y Foso (Claude, provisional) |
| `camps.level_up_cost_per_level` (nuevo) | — | 🪵30 🪨20 🌿10 × el nivel actual (de 1 a 9: 1.080 de madera, 720 de piedra y 360 de fibra) (Claude, provisional) |
| `camps.chests_from_level` / `chests_per_level` | 6 / 1, los pagaba quien agrandaba | los mismos números; ahora los pide ⏫ Siguiente nivel y los aportan todos con 🤲 (6 cofres hasta castillo, como antes) |
| `camps.territory_map_radius` (nuevo) | — | 2: el minimapa de 🗺️ Agrandar territorio es de 5 × 5 (Claude) |

**Qué cambia al jugar.**

- Subir de nivel ya no es pagar y listo: pide construir antes las obras de la lista (17 obras nombradas hasta castillo, de 1 a 3 por nivel; el castillo ya pedía 15 construidas) y materiales que pone todo el campamento.
- Hasta castillo, sumando los dos caminos (el nivel y 24 zonas más), son unas 5.580 maderas, 3.720 piedras y 1.860 fibras. Antes eran 560, 370 y 180 para 9 zonas y el nivel 9.
- Un campamento de nivel 1 puede tener 3 zonas sin subir de nivel; uno de aldea, 5.

**Lo que queda por mirar:**

- Si las obras de la lista traban a los campamentos chicos (la Biblioteca del nivel 7 es cara).
- Si 25 zonas a 15 × zonas cada una es demasiado caro al final (la 25.ª cuesta 🪵360).
- Si conviene que la muralla de D-254 use el mismo tope.

### Octubre de 2026 (20-oct): el chat del gremio (0.40, D-302)

| Número | Antes | Ahora |
|---|---|---|
| `gremio.messages_kept` | 5 | 50 mensajes guardados |
| `gremio.chat_hours` (nuevo) | — | 24: el 📢 Chat muestra los del último día |
| `gremio.chat_shown` (nuevo) | — | 20 como mucho |
| `gremio.chat_max_chars` (nuevo) | — | 3.500 letras (para que entre en un mensaje de Telegram) |

### Octubre de 2026 (20-oct): más madera (0.40, D-300)

| Número | Antes | Ahora |
|---|---|---|
| `resources.wood.forest` (nuevo) | — | bosque, bosque oscuro y selva: siempre con madera (Claude, sobre el pedido del dueño) |
| `resources.wood.forest_min` (nuevo) | — | 0,7: riqueza mínima de la madera en esos terrenos |
| `resources.wood.threshold` (nuevo) | — | 0,62 (igual al general): fuera del bosque, la madera entra donde ya era fuerte pero el tope de 3 la dejaba afuera |
| `stock.regen_mult.madera` (nuevo) | ×1 (1 por hora por zona) | ×2 (unas 2 por hora por zona); se suma al ⛲ Pozo |

**Qué cambia al jugar.** Zonas con madera, medido en 73 × 73 zonas con 3 semillas:

- **Todo el mapa:** del 39-47 % al 55-63 %.
- **En los bosques:** del 40 % al 100 %.
- **Fuera de ellos:** sube unos 3 puntos.

Desde casi todas las fogatas hay madera a 1 zona. Solo se suma madera, sin quitar ningún recurso ni mover nodos. Lo que cambia es el orden en que se descubren: la madera va justo después de los recursos de base.

**Lo que queda por mirar:** si alcanza para las obras; si hace falta un botón 🪓 Talar (P-238).

> **Desde la 0.41.1 (D-303)** `forest_min` sube a 1,0 y `threshold` queda sin uso: la madera ya está en todas las zonas (abajo).

### Octubre de 2026 (20-oct): madera en todas las zonas (0.41.1, D-303)

El dueño: "los bosques deberían tener, las montañas deberían tener, o sea, en todos lugares, en menor medida, pero deberían tener". Los números son de Claude (provisionales).

| Número | Antes | Ahora |
|---|---|---|
| `resources.wood.forest_min` | 0,7 | 1,0: en el bosque, bosque oscuro y selva la madera es la más rica y va **primera** (se conoce al 1 %) |
| `resources.wood.elsewhere_max` (nuevo) | — | 0,5: en los demás terrenos, si la madera no era de base, se suma pobre (de 0,3 a 0,5 según su fuerza en la zona) |
| `resources.wood.threshold` | 0,62 | sin uso: ya no hay umbral, la madera está en todas las zonas |
| `gremio.search_rich_penalty` (nuevo) | — (solo la distancia) | 4: el 🔎 buscador cuenta cada zona como si estuviera (1 − riqueza) × 4 zonas más lejos: primero las cercanas y ricas |
| `exploration.reveal_at` (regla, no número) | la madera sumada ocupaba un lugar | la madera sumada no ocupa un lugar: se conoce junto con el recurso que tocaba (nadie conoce menos que antes) |

**Qué cambia al jugar.** Medido en 61 × 61 zonas con las semillas 12345, 777 y 4242 (riqueza completa, sin agotar; "antes" es sin D-300):

| | Zonas con madera (antes / 0.40 / 0.41.1) | Madera en cada unidad recolectada (antes / 0.40 / 0.41.1) | Se conoce al 1 % (0.40 / 0.41.1) |
|---|---|---|---|
| Bosques (23 % de las zonas) | 47 % / 100 % / 100 % | 11 % / 20 % / 23 % | 25 % / 100 % |
| Los demás terrenos | 46 % / 49 % / 100 % | 11 % / 12 % / 17 % | 24 % / 24 % |
| Fogatas (fijas) | 100 % | 56 % | 100 % |

- **Toda zona que no es fija tiene madera** (3.712 de 3.712 en cada semilla).
- Fuera del bosque hay dos casos: donde la madera ya era de base (46 % de esas zonas) sigue igual, riqueza media 0,93 y 24 % de cada unidad, como en el bosque; donde se suma, riqueza media 0,42 y 10 % de cada unidad.
- Solo se suma madera: ninguna zona pierde un recurso ni la riqueza de otro, y los nodos no se mueven.

**Lo que queda por mirar:** en el bosque, 1 de cada 4 unidades es madera, y en la fogata más de la mitad (sus 2 recursos fijos). Si hace falta más, lo que queda abierto en P-238: el botón 🪓 Talar (solo madera) y que los recursos de base vuelvan más rápido.

> **Desde la 0.42 (D-305)** las dos cosas están en el juego (abajo).

### Octubre de 2026 (21-oct): el 🗺️ pergamino de mapa del Explorador (0.50, D-311.5 confirmada; D-326 provisional)

El dueño respondió E-180: el 🧭 Explorador hace un pergamino con las zonas que exploró al 50 % en una región de 6 × 6 y lo vende al precio que quiera. Los números son nuevos y de Claude (D-326); se ajustan en la beta (E-250, E-251).

| Número | Antes | Ahora |
|---|---|---|
| `map_scroll.rank` (nuevo) | — | 15: rango de 🧭 Explorador desde el que se hacen (entre el 10 de ⏱️ y 🔭 y el 25 de 👹 a 3 zonas; unos 1.764 de experiencia, ~300 vueltas de explorar) |
| `map_scroll.region` / `min_zones` (nuevos) | — | región de 6 × 6 de una cuadrícula fija / al menos 6 zonas investigadas por el autor al 50 % (sin contar fogatas) |
| `map_scroll.energy` / `materials` (nuevos) | — | ⚡5 / 1 🦌 piel (🥉3 de referencia) |
| `map_scroll.explorer_xp` (nuevo) | — | 30 de experiencia de Explorador por pergamino: 6 por ⚡, como explorar y 🔭 Reconocer |
| `map_scroll.price_min` / `price_max` (nuevos) | — (la banda de `market` habría sido de 🥉25 a 🥈10 con su referencia) | de 1 🥉 a 1 🥇 (10.000 🥉): precio libre, la excepción de la banda de D-26 |
| `pergamino_mapa.price` (nuevo, `content/items.yaml`) | — | 100 (1 🥈): solo el precio con el que abre el borrador del 🏛️ Mercado |

**Qué cambia al jugar.**

- **Una salida nueva para la energía del Explorador:** 5 ⚡ y una piel dan un pergamino y la misma experiencia que 5 vueltas de explorar; el pergamino vale lo que alguien pague por él (menos el 5 % del mercado, que se quema).
- **No crea monedas ni recursos:** lo que se paga lo cobra otro jugador; el comprador gana solo el color de esas zonas, no sus recursos (los sigue descubriendo explorando, con su propio porcentaje).
- **La piel tiene un uso más** (cazar bestias, D-306.5), chico: una por pergamino.
- **Lo que no cambia:** el combate, la exploración, los recursos de cada zona, el 🛒 Mercader y la banda de los demás objetos.

**Lo que queda por mirar:** cuántos pergaminos se hacen y se venden por día, a qué precio (si se juntan contra el tope de 1 🥇, E-251), si alguien pasa monedas entre cuentas con precios raros (el informe diario cuenta las ventas del mercado) y si 6 zonas o el rango 15 frenan demasiado (E-250).

### Octubre de 2026 (21-oct): el 💰 fondo del gremio para los oficios (0.47, D-322 provisional)

El dueño pidió que los del gremio "puedan primero construir las estructuras y después poder utilizar los recursos para las profesiones de cada uno". Los números son nuevos y de Claude (D-322); se ajustan en la beta.

| Número | Antes | Ahora |
|---|---|---|
| `fund_crafts.daily_cap` (nuevo) | — | 40 unidades del fondo por miembro y por día real, todos los materiales juntos (unos 13 tablones, o un par de piezas de equipo de nivel bajo) |
| `fund_crafts.default_open` (nuevo) | — | `true`: el fondo para oficios empieza 🔓 abierto; el fundador o un 🤝 asistente lo cierra |
| `fund_crafts.log_kept` / `log_shown` (nuevos) | — | 20 líneas guardadas / 10 en pantalla (📜 Quién usó qué) |

**Qué cambia al jugar.**

- **Nada sale del juego ni entra:** el material del fondo lo juntaron los miembros; ahora, además de las obras, puede ir a sus oficios. No se crean monedas ni materiales.
- **Las obras no esperan más que antes:** la reserva (lo que les falta a las obras activas y a ⏫ Siguiente nivel) nunca se usa para oficios.
- **Un artesano del campamento sube más rápido:** con el fondo lleno, hasta 40 unidades por día más de material para refinar o fabricar (con una receta de 3 maderas por tablón, 13 vueltas de 1 ⚡ y ~78 de experiencia de oficio). El freno es el tope y su ⚡.
- **Lo que no cambia:** lo que piden las obras y el nivel, el 🏛️ Mercado (el fondo no se vende ahí) y el combate.

**Lo que queda por mirar:** cuánto se toma por día y por campamento, cuántos llegan al tope, cuántos campamentos lo cierran y si las obras nuevas se quedan sin material porque lo que sobraba se usó antes de activarlas (P-251).

### Octubre de 2026 (21-oct): el 🏛️ Mercado entre jugadores (0.46, D-137 y D-26 confirmadas; D-320 provisional)

El dueño pidió un mercado entre jugadores "que funcione y luego vamos arreglando". Todos los números son nuevos y de Claude (D-320), con las referencias de [Economía](../07-economia/economia.md) §3 y §5; se ajustan con la sección 9 del informe diario.

| Número | Antes | Ahora |
|---|---|---|
| `market.tax` (nuevo) | — | 0,05: el 5 % de cada venta, lo paga quien cobra y se quema (redondeado a la unidad: una venta de menos de 10 🥉 no paga). Sin tasa por publicar (economía §5 proponía 1,5 % + 4 %) |
| `market.delivery_minutes` (nuevo) | — | 30: lo comprado llega a 📦 Entregas a los 30 min, igual para todos (D-137, sin distancia por ahora) |
| `market.order_days` (nuevo) | — | 7 días, como economía §3 |
| `market.max_orders` / `max_units` (nuevos) | — | 10 órdenes activas por jugador (ventas y pedidos juntos) / 500 unidades por orden |
| `market.price_min` / `price_max` (nuevos) | — | 0,25 / 10 veces el precio de referencia (D-26): una 🧪 poción de vida (🥉6) va de 🥉1 a 🥉60; una 💰 bolsa (🥉114) de 🥉28 a 🥈11 🥉40 |
| `market.price_buttons` / `ask_buttons` / `per_page` / `log_days` (nuevos) | — | ×1, ×2, ×3 / 1, 10, 50 unidades / 8 líneas por página / 30 días de cuenta diaria |

**Qué cambia al jugar.**

- **Una fuente nueva de monedas para los artesanos, sin crear monedas:** lo que paga un jugador lo cobra otro; solo el 5 % sale del juego. Hasta hoy, el equipo y las pociones solo se vendían al 🛒 Mercader (a la mitad, y las pociones a un cuarto); ahora se pueden vender más caro a quien los necesite.
- **Un sumidero chico:** el 5 % de cada venta. Con pocos jugadores mueve poco; crece con el comercio.
- **Los recursos tienen comprador:** quien junta puede venderle a un pedido de compra por encima de lo que paga el mercader (la banda llega hasta 10 veces la referencia).
- **Lo que no cambia:** el 🛒 Mercader paga lo mismo (P-250 pregunta si deja de comprar pociones), el 💱 Comercio sigue bloqueado (D-298) y nada del combate se mueve.

**Lo que queda por mirar:** cuántas compras hay por día y a qué precio frente a la referencia, cuánto impuesto se quema, cuántas órdenes vencen sin venderse (si es la mayoría, la banda o los 7 días no sirven), y si conviene sumar la tasa por publicar (P-247).

### Octubre de 2026 (21-oct): tramos de recetas, colores y libros (0.44, D-306 confirmada; D-315 provisional)

El dueño decidió la reforma de recetas el 20-oct (E-221 a E-223): un tramo cada 5 rangos, colores de receta como en WoW y libros de recetas por tramo. Los números de experiencia y energía son de Claude (D-315), elegidos para la meta de la simulación: el especialista al 100 en ~11 meses y obligado a fabricar lo nuevo. Se recalculó con `tools/sim_oficios.py` ([Simulación](../07-economia/simulacion-oficios.md) §11).

| Número | Antes | Ahora |
|---|---|---|
| Rango de las piezas de equipo (🪑 🔨 🪡 🦺 💍) | nivel 3 → rango 1, 5 → 25, 8 → 50, 10 al 100 → 55 al 100 | nivel = rango, un tramo cada 5 (`recipe_tiers.step` 5): 3 → 1, 5 → 5, 8 → 10, 10 → 10 … 100 → 100; +180 piezas de los niveles 15, 25 … 95 |
| Energía de una pieza de equipo | 2 ⚡ | `recipe_tiers.energy_by_rank`: 2 ⚡ hasta el rango 50, 3 desde el 55, 4 desde el 85 |
| Experiencia de oficio de una pieza | 12 | 12 × (1 + 0,01 × rango) (`recipe_tiers.xp_per_rank`): 12 en el 1, 15 en el 25, 18 en el 50, 24 en el 100; muebles 24 → 34 (rango 40) y 41 (rango 70) |
| Colores (`recipe_tiers.colors`) | — (la experiencia nunca bajaba) | d = tu rango − el de la receta: 🟧 d < 5 entera, 🟨 5-9 la mitad, 🟩 10-14 un cuarto, ⬜ 15+ nada; solo en los 5 oficios de equipo |
| 📚 Libros (`recipe_tiers.books`) | — | rango 25 🥈2, rango 50 🥈10, rango 75 🥈25, uno por oficio; gratis los de los rangos que ya tenía cada uno |
| 📿 Colgante de cobre (nuevo) | — | Joyería rango 1, lingote + cuero, 2 ⚡, 12; nivel 1, vida +4 %, ataque +3 %, 🥉14 (el mercader paga 7; materiales 20) |
| Recetas de malla | 67 activas | `retired: true` (las piezas quedan) |

**Qué cambia al jugar.**

- **Especialista con los materiales en la mano:** rango 25 en 19 días (antes 22), 50 en 69 (90), 75 en 171 (205) y **100 en 329 (368)**, con ~4.600 piezas (antes 7.351 dagas). Lo que conviene es siempre la receta de su tramo: subir obliga a fabricar lo nuevo.
- **Quien junta, caza y refina todo solo:** mucho más lento que antes (2 a 4,5 veces con la misma cuenta aproximada, ya con la piel ×2,5 de la 0.43): la Herrería pasa de ~6 años a ~15-20, la Peletería de ~9 a ~20 y la Sastrería y la Joyería de ~4 a ~18-20, porque cada tramo pide más material (de 3 a 7 veces más en total, sobre todo 💠 gemas y 🌸 flores de luna: ~12.700 para un herrero o un sastre al 100). Queda para especialistas que reciben o compran materiales (P-245).
- **Experiencia de héroe al fabricar:** sube con la energía de la pieza (20 por ⚡, D-108), así que por ⚡ es la misma; una pieza de rango 85 da el doble que una de rango 1 del mismo nivel de héroe.
- **Monedas:** los libros sacan 🥈37 por oficio de quien llega al 75 (un sumidero nuevo). Las piezas nuevas se venden al mercader por menos que sus materiales (D-113), como todas.
- **Sin cambios:** el refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina siguen con su experiencia entera (sin colores) hasta tener sus tramos; sus recetas de rango 25 o más piden libro.

**Lo que queda por mirar:** cuántos compran cada libro y cuándo (informe diario); si el especialista tarda de verdad ~11 meses; si la cadena en solitario es demasiado lenta (P-245: la palanca es `xp_per_rank`); la demanda de gemas y flores de luna.

### Octubre de 2026 (21-oct): títulos de oficio, precios por rama y lo que no avanzaba (0.43, D-306, confirmada; forma: D-316)

El dueño confirmó el 20-oct (E-222, E-223, E-228) los títulos que se compran, los precios por tipo de oficio y los arreglos que recomendó la [simulación de los oficios](../07-economia/simulacion-oficios.md) §8.6. Los números de los títulos y los precios son los del dueño; el resto, de Claude (D-316, provisional).

| Número | Antes | Ahora |
|---|---|---|
| `professions.titles` (nuevo) | — (los títulos salían solos con el rango) | Oficial 🥉50 y héroe de nivel 10 · Experto 🥈2 y 20 · Artesano 🥈10 y 30 · Maestro 🥈30 y 40 · Gran Maestro 🥈50 y 50 (del dueño). Al tope (20, 40, 60, 80, 95) la experiencia de oficio no se guarda |
| `professions.learn_price` | 🥉20 todos | por rama: `craft` 100 (🥈1), `gather` 50, `refine` 50 (del dueño); `enchant` 100 y `service` 50 (Claude) |
| `professions.skinning.loot_mult.piel` (nuevo) | ×1 (1 o 2 por bestia que la suelta, 1,5 de promedio) | ×2,5 (2, 3 o 5: 3,75 de promedio) |
| `professions.skinning.xp_per_beast` (nuevo) | 0 | +3 de 🔪 Desollador por bestia que suelta carne o piel |
| `shop.remedy_sell_ratio` (nuevo) | el mercader no compraba pociones ni remedios | 0,25: 🧪 vida 🥉1 (cuesta 🥉6), 🩹 venda 🥉1 (🥉3), 🍷 mayor 🥉4, 🫙 ungüento 🥉2, 🧰 botiquín 🥉4, 🩻 vendaje maestro 🥉7 |
| `camp_professions.maintenance` (nuevo) | — | 🧱 Mantenimiento: 🪵15 🪨15 🧵10 por vuelta (40 de 🏗️ Construcción), desde 1 obra construida |
| 🎣 Pescar (regla, sin número nuevo) | — | una vuelta de recolectar (`gather.amount`, 1 a 3 más 1 cada 3 niveles de zona; 1 ⚡; 8 min) en la que toda unidad es 🐟 pescado; solo agota el pescado (vuelve ×1, 2 % por hora) |

**Qué cambia al jugar.**

- **Títulos:** subir un oficio al 100 cuesta en total 🥈92,5 en títulos (🥉9.250) y pide un héroe de nivel 50. Para el que va al ritmo de diseño (rango 25 en ~3 semanas, 50 en ~3 meses, 100 en ~1 año, `rank_formula`) y sube de nivel al ritmo de siempre (nivel 10 en ~18 días, 20 en ~70), el nivel casi nunca frena: el Oficial (rango 20, ~2 semanas) llega con el héroe cerca del nivel 10; el Experto (rango 40, ~2 meses) con el nivel 20. Quien sube un oficio muy rápido sin pelear ni explorar sí espera al héroe: es lo que pidió el dueño ("el oficio acompaña al héroe"). Es una salida de monedas que se nota, como querían E-222 y E-228.
- **Precios:** aprender los 8 oficios de fabricación cuesta 🥈8 (antes 🥉160); los 11 de recolección, refinado y servicio, 🥉550 (antes 🥉220).
- **🦌 Piel:** en las mejores zonas, de 0,45 a ~1,1 pieles por presa: de ~4,4 ⚡ por piel a ~1,8, cerca del 1,5-2 que pedía la simulación. La cadena de cuero (Curtiduría, Peletería, Herrería, arcos) deja de esperar la piel.
- **🔪 Desollador:** por presa, de ~1,05 unidades (0,53 por ⚡) a ~1,7 unidades más ~2,1 por bestia desollada (7 de cada 10 sueltan algo): ~1,9 por ⚡, como los demás recolectores (~2).
- **🎣 Pescador:** pescando, unas 2 unidades por ⚡ en una zona cercana (antes 0,66 en la mejor zona, recolectando): ~3 veces más rápido. Una zona llena aguanta unas 42 unidades seguidas y después vuelve 1 por hora.
- **🏗️ Construcción:** el catálogo entero daba como mucho rango 24; con 🧱 Mantenimiento, el rango 100 (88.209) son unas 2.200 vueltas: ~1 a 1,5 años aportando lo de un día, como decía el diseño. Gasta 🪵 🪨 🧵 (sumidero) y da la experiencia y el mérito de siempre por material.
- **🧪 Mercader:** un alquimista que hace de más recupera poco (🧪 vida 🥉1 frente a sus materiales, ~🥉6 vendidos sueltos): sirve para no tirar lo que sobra, no para hacer monedas. Nunca paga más de lo que cobra.

**Lo que queda por mirar:** si en el tope la gente siente que pierde la experiencia (la otra forma es guardarla para cuando compre el título, P-244); si 🥈92,5 por oficio es mucho o poco frente a lo que entra (informe diario); si con la piel ×2,5 sobra piel para el mercader; cuánta gente pesca y si el pescado se agota en las zonas cercanas.

### Octubre de 2026 (21-oct): 🪓 Talar y los recursos de base ×3 (0.42, D-305, confirmada)

El dueño eligió las dos recomendaciones de E-227 (20-oct): el botón 🪓 Talar y que los 6 recursos de base vuelvan 3 por hora. La forma de aplicarlo es de Claude (D-314, provisional).

| Número | Antes | Ahora |
|---|---|---|
| `stock.regen_mult.madera` | ×2 (D-300: unas 2 por hora por zona) | ×3: unas 3 por hora por zona (6 % por hora) |
| `stock.regen_mult` de piedra, fibra, hierba curativa, metal y arcilla (nuevos) | ×1 (1 por hora por zona) | ×3 (3 por hora por zona) |
| Recursos propios del terreno y 🐟 pescado | ×1 | ×1 (sin cambio: no están en `regen_mult`) |
| 🪓 Talar (regla, sin número nuevo) | — | una vuelta de recolectar (`gather.amount`, 1 a 3 más 1 cada 3 niveles de zona; `energy.per_gather` 1 ⚡; `gather.minutes` 8) en la que toda unidad es 🪵 madera; solo agota la madera; ×2 en un nodo de madera (`nodes.yield_mult`) |

**Qué cambia al jugar.**

- **Vuelve más rápido:** un recurso de base que se agotó al recolectar (justo bajo el 15 %, `stock.min_yield`) vuelve a dar en unos 10 minutos; de vacío a lleno tarda unas 17 horas (antes 50; la madera, 25). Cada zona da por día unas 72 unidades de cada recurso de base que tenga (antes 24; la madera, 48). Con el ⛲ Pozo, ×1,5 encima.
- **Madera por ⚡:** recolectando en el bosque, 1 de cada 4 unidades es madera (unas 0,5 por ⚡ en una zona de nivel 1); talando, todas (unas 2 por ⚡, 4 veces más; en los demás terrenos, unas 6 veces más). Una zona llena aguanta unas 42 unidades seguidas (unas 21 vueltas) antes de agotarse; después, 3 por hora.
- **Leñador:** sube 1 por unidad de madera (`professions.gather_xp_per_unit`), así que talar lo sube unas 4 veces más rápido que recolectar en el bosque.

**Lo que queda por mirar:** si con 3 por hora y 🪓 Talar sobra madera para las obras (si sobra, se puede bajar a ×2); si el bosque pierde valor al talar, porque la riqueza no cambia cuánto sale (P-242); cuánto talan los jugadores en el informe diario.

### Octubre de 2026 (19-oct): el buscador de recursos (0.39.1, D-296, confirmada)

| Número | Antes | Ahora |
|---|---|---|
| `gremio.search_min_pct` (nuevo) | — | 50: el 🔎 buscador solo muestra zonas investigadas al 50 % o más (lo dijo el dueño) |

**Qué cambia al jugar.** Nada de balance: encontrar un recurso conocido es más rápido. Con 50 % se conocen los 3 primeros recursos de la zona (`exploration.reveal_at`); los demás aparecen al seguir explorando.

### Octubre de 2026 (21-oct): los edificios de oficio piden lo de su oficio (0.45, D-317, confirmada)

**Por qué.** El dueño pidió que cada edificio de oficio se construya sobre todo con los materiales de ese oficio y solo un poco de madera y piedra (90 % y 10 %). Se mantuvo el valor en crudo de cada obra para no alargar el camino al castillo.

| Edificio | Antes | Ahora (en crudo) |
|---|---|---|
| Aserradero | madera 25, piedra 10 | tablón 10, madera 2, piedra 2 (34) |
| Tejeduría | fibra 20, madera 20 | tela 12, madera 2, piedra 2 (40) |
| Cantería | piedra 25, madera 15 | sillar 12, madera 2, piedra 2 (40) |
| Curtiduría | madera 30, piedra 15, piel 10 | cuero 25, madera 3, piedra 2 (55) |
| Alambique | piedra 25, arcilla 15, hierba 15 | extracto 16, madera 3, piedra 3 (54) |
| Fundición | piedra 30, arcilla 15, metal 10 | lingote 25, madera 3, piedra 2 (55) |
| Carpintería | madera 60, piedra 20, fibra 20 | tablón 30, madera 5, piedra 5 (100) |
| Sastrería | fibra 60, madera 30, arcilla 15 | tela 32, madera 5, piedra 5 (106) |
| Peletería | madera 50, piel 30, fibra 30 | cuero 35, tela 10, madera 5, piedra 5 (110) |
| Alquimia | hierba 40, arcilla 40, piedra 30 | extracto 28, arcilla 15, madera 6, piedra 5 (110) |
| Botica | hierba 50, madera 40, fibra 30 | extracto 25, tela 11, madera 6, piedra 6 (120) |
| Forja | piedra 80, madera 50, metal 40 | lingote 60, cuero 15, madera 10, piedra 10 (170) |
| Joyería | piedra 60, arcilla 40, metal 30 | lingote 58, madera 7, piedra 7 (130) |

Las monedas no cambian. Las obras activadas o empezadas antes de la 0.45 siguen pidiendo lo de antes (`cost_before`).

**Qué cambia al jugar.** Construir un edificio de oficio pide refinar antes (1 ⚡ por pieza), y gana peso tener a alguien con ese oficio en el gremio (D-168). La demanda se mueve de la piedra y la madera a la **piel** (Curtiduría y Peletería: 120 pieles en total, antes 40) y al **metal** (Fundición, Forja y Joyería: 286 piezas en total, antes 80).

**D-318, en la misma 0.45: desde el nivel 5 las obras mezclan oficios.**

| Edificio | Antes | Ahora |
|---|---|---|
| Muralla | piedra 260, madera 60, arcilla 40 | piedra 210, madera 60, arcilla 40, 🪑 Paveses de roble 1 |
| Huerto | madera 80, fibra 60, hierba 50, arcilla 40 | madera 45, fibra 60, hierba 50, arcilla 40, 🪑 Carro de víveres 1 |
| Braseros | madera 120, piedra 120, metal 50 | madera 120, piedra 120, metal 20, lingote 15 |
| Enfermería | tablón 40, madera 60, fibra 100, hierba 100, sillar 20, piedra 20 | tablón 40, madera 30, fibra 40, hierba 40, sillar 20, piedra 20, 🪑 Literas de roble 1, ungüento 10, venda 10 |
| Biblioteca | tablón 60, madera 40, sillar 40, piedra 30, fibra 100, arcilla 60 | tablón 60, madera 40, sillar 40, piedra 30, tela 30, arcilla 30, extracto 10 |
| Torres de arqueros | tablón 80, madera 40, sillar 40, piedra 30, metal 70, fibra 60 | tablón 60, madera 40, sillar 40, piedra 30, metal 65, fibra 60, 🪑 Armero de roble 1 |
| Foso | sillar 100, piedra 60, arcilla 140, tablón 25, madera 25 | sillar 100, piedra 60, arcilla 120, tablón 25, madera 25, lingote 10 |

**Lo que queda por mirar:** si la piel y el metal frenan los campamentos (los dos son más escasos que la piedra); si conviene una pequeña rebaja en esas tres obras; si los 🪑 muebles que piden las obras de nivel alto llegan a tiempo (la 🪑 Carpintería tiene que existir en el gremio). *Lo midió la 0.45.1 (D-319, el bloque siguiente): los muebles trababan la subida de nivel y se cambiaron; la piel ×2,5 de la 0.43 y el metal ×3 de la 0.42 compensan casi todo.*

### Octubre de 2026 (21-oct): recálculo de costos y beneficios de los edificios (0.45.1, D-319, provisional)

**Por qué.** Después de la 0.45 el dueño pidió (por otra sesión) "recálculo y ajuste de costos y beneficios de los edificios": si la piel y el metal frenan, si los 🪑 muebles que piden las obras de nivel alto llegan a tiempo y si cada edificio vale lo que cuesta. Se midió con `python tools/camp_costs.py` (nuevo; sus supuestos, en el encabezado).

**Supuestos.** ~4,7 unidades de recurso de base por ⚡ en tu territorio (zona de nivel 3: `gather.amount` 1 a 3, +1 por el nivel, × `gather.own_land_bonus` 1,5, redondeado como el juego); 🦌 piel 1,76 ⚡ y 🍖 carne 3,3 ⚡ cazando fuera del territorio (la simulación del 18-oct, con la piel ×2,5 de la 0.43); refinar y fabricar, el ⚡ de su receta (1 por pieza refinada); cada miembro da 30 ⚡ por día (75 % de `energy.per_day`); 5 miembros en los niveles 1 y 2, 6 en el 3, 8 en el 4 y 10 desde el 5; las obras una tras otra con el +15 % por obra construida (D-295) y ⏫ `camps.level_up_cost_per_level` × nivel (D-304). Quedan fuera, sin cambios: los 6 🪎 cofres, la 🌙 Noche de prueba y 🗺️ Agrandar territorio.

**Del campamento al castillo.** "Lista" son las 17 obras que pide ⏫ Siguiente nivel (el castillo no pide otras: ya son más que `castle_min_built`); "las 31" suma los 13 edificios de oficio y el 🏪 Trueque.

| Camino | Versión | En crudo | 🦌 piel | ⚙️ metal | ⚡ total (juntar + refinar y fabricar) | 🥉 | Días | Lo más alto que pide |
|---|---|---|---|---|---|---|---|---|
| Lista (castillo) | antes de la 0.45 | 13.585 | 0 | 397 | 4.417 (3.115 + 1.302) | 2.435 | 15,9 | refinado de rango 1 |
| Lista (castillo) | 0.45 | 13.510 | 72 | 521 | 5.020 (3.210 + 1.810) | 2.435 | 17,9 **+ meses de espera** | 🪑 Carpintería 70, y 🎓 Escudos (50) y 🎓 Mobiliario (25): dos carpinteros |
| Lista (castillo) | **0.45.1** | 13.447 | 36 | 539 | 4.928 (3.141 + 1.787) | 2.435 | **17,6** | 🪑 Carpintería 15 (un carpintero dedicado: 7 días) |
| Las 31 obras | antes de la 0.45 | 25.278 | 137 | 1.013 | 8.112 (5.959 + 2.153) | 7.997 | 30,0 | refinado de rango 1 |
| Las 31 obras | 0.45 | 25.159 | 632 | 2.080 | 11.160 (6.698 + 4.462) | 7.997 | 42,3 + espera | lo mismo que arriba |
| Las 31 obras | **0.45.1** | 25.062 | 434 | 2.250 | 10.799 (6.371 + 4.428) | 7.997 | **41,1** | 🪑 Carpintería 15 |

Con la mitad de la energía de cada miembro (`--share=0.5`): la lista, 23,8 / 26,9 / 26,4 días; las 31, 45 / 63 / 62.

**El camino de la lista, hoy:** nivel 5 hacia el día 4, 6 hacia el 5,5, 7 hacia el 6,5, 8 hacia el 11 y castillo hacia el 17,6. En la 0.45 se trababa en el nivel 5: la 🧱 Muralla y el 🥬 Huerto (los dos obligatorios para subir a 6) pedían muebles de especialista.

**1. Piel y metal.**

- **Piel:** un campamento completo pedía 632 en la 0.45 (antes 137: ×4,6), sobre todo por el crecimiento (la 🦺 Peletería, hecha como obra 20.ª, pide ×3,85: 135 cueros, 270 pieles). Contado en energía: 137 × 4,4 ⚡ = 603 ⚡ antes de la 0.43; 632 × 1,76 = 1.112 ⚡ en la 0.45 (×1,8). Con la 0.45.1 (la 🔨 Forja sin cuero y sin los muebles de la Muralla y el Huerto), 434 pieles = 764 ⚡ (×1,3): **la piel ×2,5 de la 0.43 compensa casi todo**. El camino al castillo pide solo 36 (las 🛏️ Literas y el 🗄️ Armero).
- **Metal:** de 1.013 a 2.080 (0.45) y 2.250 (0.45.1: la Forja pide 75 lingotes): ×2,2, mientras la 0.42 triplicó lo que vuelve (cada zona con metal da unas 72 piezas por día, 108 con el ⛲ Pozo). En energía son ~260 ⚡ más de juntar (2 % del total). **No se recortó.**
- **Lo que más pesa es refinar:** 1 ⚡ por pieza, más que juntar lo que lleva (3 maderas son 0,64 ⚡ en tu territorio). Por eso los 13 edificios de oficio cuestan de 2 a 4 veces la energía de antes, aunque pidan lo mismo en crudo: 🪣 Curtiduría 27 → 114 ⚡, 🦺 Peletería 70 → 177, 🔨 Forja 36 → 111 (158 en la 0.45), 💍 Joyería 28 → 86, 🩺 Botica 26 → 62, 🪡 Sastrería 22 → 55, ⚗️ Alquimia 24 → 52, 🪑 Carpintería 21 → 51, 🏭 Fundición 12 → 37, 💧 Alambique 12 → 28, 🪚 🧶 🗿 8-9 → 17-21 (de base, sin el +15 %).

**2. Los muebles que pedían las obras de la lista** (días de un carpintero dedicado: todo su ⚡ a la 🪑 Carpintería, con los materiales en la mano, como `tools/sim_oficios.py`):

| Mueble | Lo que pedía en la 0.45 | Obra (sube a) | Tardaba | En la 0.45.1 |
|---|---|---|---|---|
| 🛡️ Paveses de roble | Carpintería 50, 🎓 Escudos, 📚 libro del 50 (🥈10), título Experto (héroe 20) | 🧱 Muralla (6) | ~69 días (~66.000 en crudo de lo que fabrica para subir) | ya no lo pide (🪨180 🧱10 🪵60 arcilla 40 🟫12 lingote 5); sigue como mueble de su 🎓 |
| 🛒 Carro de víveres | Carpintería 25, 🎓 Mobiliario con el 25 % de dominio (~rango 29), 📚 del 25, Oficial (héroe 10) | 🥬 Huerto (6) | ~24 días, **y otro carpintero**: una 🎓 por héroe hasta el 75 | ya no lo pide (🪵45 🌿60 hierba 50 arcilla 40 🟫10 lingote 3); sigue como mueble de su 🎓 |
| 🛏️ Literas de roble | Carpintería 40, 📚 del 25, Oficial | 🏥 Enfermería (8) | ~46 días (~40.000 en crudo) | **rango 10**: ~3 días (~1.100 en crudo), sin libro ni título |
| 🗄️ Armero de roble | Carpintería 70, 📚 del 25 y del 50, Artesano (🥈10, héroe 30) | 🏹 Torres de arqueros (9) | ~147 días (~140.000 en crudo) | **rango 15**: ~7 días (~3.800 en crudo) |

Con el +15 % por obra, cada uno se pide ×3 a ×5 (la Enfermería, hecha como obra 14.ª de la lista, pide 3 Literas, 30 ungüentos y 30 vendas; las Torres, 4 Armeros). La 🏥 Enfermería sigue pidiendo Carpintería, Medicina y Sastrería, el ejemplo del dueño (D-318). Regla nueva (D-319): lo que piden las obras de ⏫ se hace con rango 10 o menos (15 en el paso a castillo), sin 🎓, sin 📚 y sin título comprado (`tests/test_costos_edificios.py`).

**3. ¿Vale cada edificio lo que cuesta?**

- **Las 17 obras de la lista:** son obligatorias para subir, así que se miden por el ritmo: cuestan un 11 % más de energía que antes de la 0.45 (lo refinado desde el nivel 5) y no traban a nadie. Sus efectos no cambiaron.
- **Los 13 edificios de oficio:** dan la estación en casa (ahorra el viaje al Claro, que tiene todas: tiempo, no energía), la 🪡 Sastrería las bolsas y los cofres y la 🔨 Forja la venta de equipo. El castillo no los pide y **cada uno sube un 15 % lo que sigue**. Con la 0.45 cuestan de 2 a 4 veces más energía: hoy son un lujo del campamento, no el camino. Si deben dejar de encarecer lo demás lo decide el dueño (E-235, P-246; con `--growth-no-oficio`, las 31 obras bajan a ~28 días).
- **Los muebles:** las 🛏️ Literas (+1 lugar) y el 🗄️ Armero (+1 de 🛡️ Defensa) llegan antes; la obra los gasta, así que quien quiera colocar uno hace uno más.
- **Monedas:** sin cambios (2.435 🥉 en la lista; 7.997 en las 31).

**Qué cambia al jugar.**

- Ningún campamento se traba en un nivel esperando un rango alto: el carpintero del campamento llega al 10 en ~3 días y al 15 en ~7, antes de que el campamento llegue al 7 y al 8.
- La Muralla y el Huerto piden tablones, lingotes y sillares en vez de muebles de especialista; la Forja, solo lingotes.
- Las obras activadas antes conservan su costo: lo de antes de la 0.45 (`cost_before`) o el que guardaron al activarse.
- La 🪑 Carpintería sube al 75 y al 100 al ritmo de los otros oficios de equipo (171 y 329 días; antes 162 y 321, porque el Armero de rango 70 daba más experiencia por ⚡: [simulación](../07-economia/simulacion-oficios.md) §11).

**Lo que queda por mirar:** E-235 (los edificios de oficio y el +15 %); cuánta piel se junta de verdad (informe diario); si los campamentos construyen sus edificios de oficio o los dejan para el final.

### Octubre de 2026 (21-oct): la 🌾 cosecha de la muralla y adiós al +50 % del territorio (0.49, D-309 confirmada; D-325 provisional)

**Por qué.** El dueño confirmó el 20-oct (D-309, E-216 y E-217) que cada zona cerrada por la muralla cosecha sola el 20 % de lo que vuelve a crecer, al almacén del asentamiento, solo con jugadores activos esa semana y con un tope de 7 días, y que eso **reemplaza** el +50 % de recolectar en tu territorio (D-239.3: nada de bonos de farmeo aparte).

| Número | Antes | Ahora | Por qué |
|---|---|---|---|
| `gather.own_land_bonus` | 1,5 | **1,0** (la clave queda) | D-309: la cosecha lo reemplaza. En tu territorio juntas unas 3 unidades por ⚡ (antes ~4,7) |
| `harvest.share` | — | **0,20** | D-309 (E-216) |
| `harvest.real_regen` | — | **false**: 24 por recurso y día, sin el ×3 de la 0.42 ni el ⛲ Pozo | D-325: el número de la pregunta del dueño; contar el ×3 doblaría la cosecha (E-248) |
| `harvest.week_days`, `cap_days`, `active_days` | — | **7, 7 y 7** | D-309: llega cada semana, guarda como mucho 7 días y solo si alguien jugó esa semana |
| `harvest.scan_minutes` | — | 60 | D-325: cada cuánto mira `tick()`; una muralla de antes empieza a contar como mucho 1 hora antes |

**Cuánto da.** Una zona tiene hoy de 4 a 6 recursos de tierra (5,6 en promedio, 2,8 de ellos de base; medido en 432 zonas de la semilla 12345), así que da **~27 unidades por día** (la tabla de la escalera §5.3 contaba 3 recursos: 14). Con el tope de zonas de cada etapa: pueblo (9) ~240 por día, ciudad (15) ~400, castillo (25) ~670. Lo que sirve para las obras son los de base: ~120, ~200 y ~330 por día. El 🐟 pescado no entra (es comida).

**El ritmo hasta castillo** (`python tools/camp_costs.py`, que desde la 0.49 cuenta la cosecha desde el nivel siguiente al de la muralla: ahorra energía de juntar, nunca de refinar; de 5 a 10 miembros con el 75 % de su ⚡):

| Camino | 0.48 (+50 %) | 0.49 sin cosecha | **0.49 con cosecha** | Con el ×3 (E-248) |
|---|---|---|---|---|
| La lista (castillo) | 17,6 días | 23,4 | **20,7** | 17,4 |
| Las 31 obras | 41,1 | 52,1 | **47,7** | 42,4 |
| La lista, con la mitad de la energía | 26,4 | 35,2 | **29,5** | — |

Nivel por nivel (la lista, hoy): nivel 5 hacia el día 5,5 (antes 3,9), 6 hacia el 7,9 (antes 5,5), 7 hacia el 9,2, 8 hacia el 14,2 y castillo hacia el 20,7. Antes de la muralla la pérdida del +50 % no tiene vuelta (E-249); desde el pueblo, la cosecha devuelve 40 a 66 ⚡ por día en un campamento de 10 (300 ⚡ por día). Las columnas "antes de la 0.45" y "0.45" de la herramienta también cuentan ya sin el +50 % y con la cosecha.

**Qué cambia al jugar.**

- En tu territorio juntas lo mismo que afuera (siguen sin salir peleas y las ⚒️ Herramientas dan +10 %).
- Con la 🧱 Muralla, cada semana entran al 💰 fondo unos cientos de materiales sin gastar energía; van primero a las obras y a ⏫ Siguiente nivel, y lo que sobra, a los oficios (D-322).
- Un campamento de nivel 1 a 5 tarda un tercio más en juntar lo crudo; desde el pueblo, la cosecha compensa una parte.

**Lo que queda por mirar:** E-247 (qué zonas cierra la muralla), E-248 (contar el ×3) y E-249 (los niveles antes de la muralla); cuánto entra de verdad por semana y por campamento y cuántas semanas se pierden por falta de actividad (informe diario).

### Octubre de 2026 (19-oct): el campamento de la 0.39 (D-288 a D-291, D-294, D-295)

| Número | Antes | Ahora |
|---|---|---|
| `upgrades.cost_growth` (nuevo) | — | 0,15: cada obra nueva cuesta un 15 % más por cada obra ya construida; precio fijo al activarla (D-295, Claude sobre la regla del dueño) |
| `camps.helpers_per_members` (nuevo) | — | 5: 1 🤝 ayudante cada 5 miembros (D-289, del dueño) |
| `armory.slots` / `armory.log_kept` (nuevos) | — | 30 lugares en la ⚔️ Armería / los últimos 10 movimientos (D-290, Claude) |
| `gremio.waiting_max` (nuevo) | — | 10 miembros en espera de lugar en el campamento (D-294: tope fijo del dueño, el número de Claude) |
| `upgrades.type_shown` (nuevo) | — | 3 obras por página en cada tipo de 🏘️ Servicios (Claude) |
| Edificios de oficio (nuevos, `content/camp_upgrades.yaml`) | el 🧵 Taller (nivel 5) abría 10 oficios y la Herrería (6) 3 | uno por oficio: nivel 1 Aserradero, Tejeduría, Cantería (35-40 unidades); 2 Curtiduría, Alambique, Fundición (55 + 🥉30); 3 Carpintería, Sastrería (100-105 + 🥉50); 4 Peletería, Alquimia, Botica (110-120 + 🥉100); 5 Forja, Joyería (130-170 + 🥉200) |

**Qué cambia al jugar.** Un campamento chico ya refina desde el nivel 1 con el oficio que elija, sin esperar al Taller del nivel 5. El castillo sigue pidiendo 15 obras: sin `cost_growth`, las 15 más baratas costaban 1.035 unidades (antes de la 0.39, 2.445); con el 15 % por obra, unas 2.400.

**Lo que queda por mirar:** si el 15 % hace muy caras las últimas obras de un campamento grande (la 25.ª pide ×4,6); si conviene que algunas obras (las de oficio) no cuenten para el castillo.

### Octubre de 2026 (19-oct): tu gremio en el mapa (0.38.1, D-286, confirmada)

| Número | Antes | Ahora |
|---|---|---|
| `map_view.mates_listed` (nuevo) | — | 8: cuántos compañeros nombra el 🗺️ Mapa arriba de la cuadrícula (Claude) |

**Qué cambia al jugar.** Nada de balance: solo cuántas líneas lleva el mapa. Con 8 compañeros a la vista, el mapa baja 9 renglones en el teléfono.

**Lo que queda por mirar:** si con gremios grandes conviene bajar el tope o juntar varios nombres por renglón.

### Octubre de 2026 (18-oct): la vida en 30 minutos (0.38, D-284, confirmada)

| Número | Antes | Ahora |
|---|---|---|
| `regen.hp_full_minutes` | 240 (4 horas) | 30 |
| `regen.downed_full_minutes` | 500 (unas 8 horas, D-83) | 30: caer no cuesta tiempo extra |
| `inn.speed` (sin cambio) | 4: posada de 0 a llena en 1 hora | 4: de 0 a llena en 7,5 min (nunca menos de `inn.min_minutes`, 5) |

**Qué cambia al jugar.** Después de una pelea se vuelve a jugar enseguida: una vida a la mitad se llena en 15 minutos. Las pociones y las vendas valen menos para el día a día y más en medio de una pelea o de un lote largo; la posada casi no hace falta (5 a 7,5 min por 🥉4). Caer ya no deja al héroe horas afuera: lo que se pierde es lo de la derrota (monedas, el lote cortado).

**Lo que queda por mirar:** si las pociones se siguen comprando; si la posada sigue teniendo sentido o conviene darle otro uso; si sin el castigo de tiempo al caer los jugadores pelean demasiado arriba de su nivel.
