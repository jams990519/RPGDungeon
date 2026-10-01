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
| Despensa del Claro desde | aldea | §7.1: hasta campamento, subir es solo pagar (tutorial) |
| Despensa de los campamentos desde | nivel 3 | §7.2, capa ligera |
| Consumo | 1 ración por residente activo por día real | §4.2 |
| Activo | tocó un botón en las últimas 24 h (marca renovada cada 60 min) | §2.1 y §15.3: quien no juega no come |
| Despensa nueva | 7 días para todos los que podrían comer de ella | §15: nadie empieza castigado |
| Estados (días) | abundancia 14 · holgada 7 · justa 3 · escasez 1 · hambruna 0 | §3.2 |
| Días para subir el Claro | pueblo 4 · ciudad 5 · castillo 7 | "Despensa sostenida" de §7.1 corrida una etapa (la despensa se abre en aldea) |
| Experiencia y mérito por ración | 2 y 1 | Como un material de la obra común (`settlement.xp_per_unit`) |
| 🍖 Carne | 2 raciones; 40-60 % por victoria contra bestias; 1-2 piezas; se vende a 1 🥉 | §4.1 (caza), en chico |
| 🥖 Provisiones | 1 ración; 15 🥉 en el mercader; no se revenden | §15.8: comida de emergencia cara |

**Cuenta rápida.** Una victoria contra un lobo deja en promedio 0,5 × 1,5 × 2 = 1,5 raciones. Con 40 de energía por día, quien pelea seguido gana muchas más raciones de las que come (1 por día): la comida no falta si los que pelean la llevan a la despensa. Lo que se pone a prueba es la **participación**, no la producción. Alimentarse solo con provisiones cuesta 15 🥉 por persona y día (unas tres peleas tempranas de monedas).

**Lo que queda por mirar:** si la carne alcanza de sobra (bajar la probabilidad o el valor), el tope por semana de las provisiones (§15.8) y si hace falta un tope de capacidad antes de los graneros (§4.3). Medir en la beta cuántos días alcanza la despensa del Claro con la gente real.

### Octubre de 2026: jugadores en la zona (D-96, provisional)

**Por qué.** El dueño pidió por voz ver, al tocar 📍 Zona, a los otros jugadores que están en tu zona y lo que hacen, y toparte con ellos al explorar (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.13). Son números **nuevos** (`content/balance.yaml` → `presence`), propuestos por Claude. No tocan el combate, la economía ni la experiencia: solo deciden qué se muestra.

| Número | Valor | Por qué |
|---|---|---|
| Presente si tocó un botón hace menos de | 15 minutos | Lo bastante corto para que la lista sea "quién está ahora"; quien explora, recolecta o duerme ahí cuenta aunque no toque botones |
| Nombres en 📍 Zona | 5, y "… y N más" | Pantallas cortas (D-86): el bloque suma como mucho 7 líneas |
| Cruce por vuelta de exploración o recolección | 15 % | Con alguien presente todo el lote, 10 vueltas dan en promedio 1,5 sorteos ganados; como a cada jugador te lo cruzas una sola vez por lote, el resumen suma pocas líneas |

**Lo que queda por mirar:** en la beta, si el Claro se llena (más de 5 presentes seguido) y conviene mostrar primero a los que hacen algo, o subir el tope.
