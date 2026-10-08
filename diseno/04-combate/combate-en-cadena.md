# Combate en cadena: las 6 clases del parche 0.31

> **Módulo** [04 · Combate](README.md) · **Depende de:** [Ronda y acciones](ronda-y-acciones.md), [Clases](../03-personaje/clases-y-especializaciones.md), [Balance](../03-personaje/balance.md) · **Alimenta a:** [Jefes](../06-contenido/jefes.md), [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md), [PvP](../06-contenido/pvp.md) · **Estado:** confirmado por el dueño (8-oct-2026) y en el juego desde la 0.31

El dueño mandó el parche completo del sistema de clases: "esto no es un resumen, es el parche completo del sistema de clases. Reemplaza lo que haya de clases y combos". Este documento lo ordena y dice cómo quedó en el juego. Las decisiones son D-225 a D-232 en [Decisiones](../00-vision/decisiones.md).

Lo firme y lo que es borrador:

- **Firme:** la estructura de la cadena, los costos y los combos.
- **Borrador, se puede ajustar:** los nombres de las habilidades y los porcentajes.
- **Configurable, sin inventar:** los pendientes del §9. Viven en `content/balance.yaml` → `chain`.

## 1. Reglas universales del combate

Las 6 clases usan la misma mecánica: 4 botones de habilidad, una cadena con dependencias y marcas que se cobran en el gastador. Solo cambia qué hace cada botón y el orden que exige cada rol.

| Botón | Papel | Costo | Requisito |
|---|---|---|---|
| Básico (B) | Arranque y recarga | 0, y da +1 de energía extra | Ninguno |
| H1 · Constructor | Relleno que carga | 2 | El eslabón que pida su rol |
| H2 · Preparador | Monta el combo o aplica el efecto | 3 | El eslabón que pida su rol |
| H3 · Gastador | El bombazo: cobra las marcas | 6 | La cadena completa del rol para cobrar el premio |

- **Energía:** la pelea arranca con 5 y se ganan 2 por turno. No hay tope.
- **Defenderse o tomar una poción** es la acción del turno y cuesta 1 de energía.
- **Tope de objetivos:** ninguna habilidad en área o a varios jugadores toca a más de 5 a la vez, en ninguna clase. En grupos grandes esto obliga a llevar más de un sanador.

## 2. Dependencia de cadena

La regla es la misma para las 6 clases; solo cambia el orden según el rol.

- Si un botón rompe el orden, la cadena se corta y se pierden las marcas acumuladas.
- Una vez cumplido el orden, se pueden repetir eslabones antes del gastador. A eso se le llama **tejer**.

| Rol | Orden | Por qué |
|---|---|---|
| Tanque | B → H2 → H1 → H3 | El básico agarra el 50 % del agro, la defensa sube temprano para aguantar el arranque caótico y el gastador fija el 100 % |
| Sanador | B → H1 → H2 → H3 | El básico recarga, la curación chica estabiliza, el preparador monta y la curación grande cobra |
| DPS | H1 → H2 → H3 (básico libre) | El camino más directo al bombazo |
| Soporte | H2 → H1 → H3 | Primero aplica su efecto, luego carga y luego lo potencia |

## 3. Marcas y bonos

Cada botón correcto de la cadena suma una marca. Al soltar el gastador se cobran todas y la cadena vuelve a cero.

| Marcas | Premio (borrador) |
|---|---|
| 2 | +10 % |
| 3 a 4 | +25 % |
| 5 o más | +50 % |

El premio se aplica a lo que hace cada rol:

| Rol | A qué se aplica el premio |
|---|---|
| DPS | Daño |
| Sanador | Sanación |
| Tanque | Agro y defensa |
| Soporte | Potencia y duración del efecto |

Reglas de las marcas:

- **Básicos seguidos cuentan como una sola marca.** No se puede hacer básico, básico, gastador para ganar el premio fácil.
- **Gastador sin combo:** pega al 80-90 % en vez del 100 %. Un combo válido exige al menos 3 botones distintos. Si se suelta el gastador sin haber usado antes la H1 o la H2, sale a ese 80-90 %.
- **Bono por variedad:** el juego anota las combinaciones distintas que usa el jugador. Mientras más use, cultiva un bono de +2 % o +3 % en lo que haga su rol.
- **Cada preparadora (H2) deja algo concreto que se nota el turno siguiente.** Ejemplos: la de sombra potencia el siguiente daño de sombra; la del Chamán deja una oleada que refuerza la siguiente curación grande.

## 4. Tres combos por rol

Verificados turno a turno, arrancando con 5 de energía y +2 por turno. B es el Básico.

| Rol | Rápido | Largo | Carga |
|---|---|---|---|
| Tanque | B → H2 → H1 → H3: 4 marcas, termina con 3 de energía | B → H2 → H1 → B → H1 → H3: 6 marcas, termina con 6 | B → B → B → H2 → H1 → H3: 4 marcas, termina con 9 |
| Sanador | B → H1 → H2 → H3: 4 marcas, termina con 3 | B → H1 → B → H2 → H1 → H3: 6 marcas, termina con 6 | B → B → B → H1 → H2 → H3: 4 marcas, termina con 9 |
| DPS | H1 → H2 → H3: 3 marcas, termina con 0 | H1 → B → H2 → B → H1 → H3: 6 marcas, termina con 6 | B → B → H1 → H2 → H3: 4 marcas, termina con 6 |
| Soporte | H2 → H1 → H3: 3 marcas, termina con 0 | H2 → B → H1 → B → H1 → H3: 6 marcas, termina con 6 | B → B → H2 → H1 → H3: 4 marcas, termina con 6 |

- **Rápido:** cobra pronto, con poco premio.
- **Largo:** da el premio gordo, pero expone al jugador más turnos.
- **Carga:** sacrifica marcas para dejar energía y encadenar otro gastador enseguida.

Los 12 combos están en `tests/test_cadena.py` y dan exactamente estos números.

## 5. Regla madre de balance

Ninguna clase nace más fuerte que otra. Las clases de un mismo rol comparten el mismo esqueleto y los mismos números base. Lo único que hace más fuerte a un personaje es la calidad de su equipo y su nivel.

| Rol | Igual para todos | Lo que cambia (el sabor) |
|---|---|---|
| Tanque | Supervivencia total | Esquiva (Druida) o placa (Guerrero) |
| Sanador | Sanación total por energía | Concentrada en uno (Sacerdote) o repartida (Chamán) |
| DPS | Daño total por rotación | Sangrado, quemadura o golpe directo |
| Soporte | Valor de apoyo | Sube aliados (Cazador) o baja enemigos (Mago) |

- La esquiva del Druida es la misma mecánica que el aguante del Guerrero: mismo resultado de supervivencia y mismo daño recibido. Solo cambian el nombre y la descripción.
- La diferencia entre dos personajes del mismo rol viene de los puntos que cargan. Gana el equipo, no la clase.
- La personalización la pone el jugador con su equipo: crítico, defensa, penetración, celeridad y versatilidad.

## 6. Progresión en tres etapas

1. **Tutorial:** el jugador recibe un arma inicial con daño bajo. Todas las clases pegan desde el principio.
2. **Nivel 5, doble especialización:** el jugador aprende su segundo rol. Al cambiar de rol se recogen y se reparten de nuevo los puntos de nivel y de mejora de habilidad.
3. **Nivel 10, modo híbrido:** el jugador elige jugar híbrido o normal. El híbrido le deja mezclar habilidades de sus dos roles. Que pueda mezclarlas no garantiza que funcionen bien: la mezcla corre por cuenta del jugador y el juego no la balancea.

## 7. Las seis clases

| Clase | Armadura | Rol 1 (orden) | Rol 2 (orden) |
|---|---|---|---|
| 🏰 Guerrero | Placa | 🛡️ Tanque de aguante (B → H2 → H1 → H3) | ⚔️ DPS de fuerza (H1 → H2 → H3) |
| 🌳 Druida | Cuero | 🐻 Tanque de esquiva, forma de oso | 🐈 DPS de sangrado, forma felina |
| 📿 Sacerdote | Tela | ✨ Sanador de uno; estadística principal: Espíritu | 🌑 DPS de sombra |
| 🌩️ Chamán | Cuero | 🌊 Sanador de grupo; estadística principal: Restauración | ⚡ DPS de rayo |
| 🏹 Cazador | Cuero | 🦅 Soporte que potencia aliados | 🏹 DPS de agilidad a distancia |
| 🔮 Mago | Tela | 🔮 Soporte que debilita al enemigo | 🔥 DPS de fuego |

| Rol | Básico | H1 · Constructor | H2 · Preparador | H3 · Gastador |
|---|---|---|---|---|
| Guerrero · Tanque | Golpe de escudo: daño bajo, 50 % del agro | Revés: daño moderado, amenaza alta | Interponerse: recibes los golpes del aliado y subes tu defensa | Grito de dominio: fija el 100 % del agro; la defensa escala con las marcas |
| Druida · Tanque | Zarpazo | Vapulear: cada esquiva mientras dura suma una marca extra | Piel de corteza: sube la esquiva 2 turnos | Rugido salvaje: fija el agro y devuelve un contragolpe por cada esquiva acumulada |
| Sacerdote · Sanador | Castigo | Renovar: curación chica y un poco más el turno siguiente | Escudo sagrado: absorbe daño | Sanación superior: toda la curación en uno (90 a uno contra 30+30+30) |
| Chamán · Sanador | Choque de tierra: arranca el combo | Sanación en cadena: 3 objetivos parejos | Golpe de tormenta: daño medio que prepara la curación grande | Marea de sanación: hasta 5 jugadores; escala solo con Restauración y con cuántos haya |
| Guerrero · DPS | Tajo | Golpe heroico | Desgarrar armadura: baja la defensa 3 turnos | Ejecutar: pega más con el enemigo bajo |
| Druida · DPS | Arañazo | Triturar | Desgarrar: sangrado cada turno | Mordisco feroz: consume el sangrado y lo cobra de una vez |
| Sacerdote · DPS | Toque mental | Tortura mental | Dolor sombrío: sombra cada turno | Explosión mental: más por cada turno de Dolor sombrío |
| Chamán · DPS | Descarga | Rayo | Choque de llamas: deja al enemigo cargado | Cadena de relámpagos: salta a varios enemigos (máximo 5) |
| Cazador · Soporte | Disparo automático | Disparo arcano: alarga la Marca de manada | Marca de manada: un aliado pega más 2 turnos (va primero) | Llamada salvaje: potencia a todo el grupo (máximo 5) |
| Mago · Soporte | Proyectil arcano | Lentitud: reduce el daño del enemigo y alarga la Fragilidad | Fragilidad arcana: el enemigo recibe más daño 2 turnos (va primero) | Ruptura arcana: baja la defensa y el daño del jefe e interrumpe su ataque cargado |
| Cazador · DPS | Disparo | Disparo firme | Marca del cazador: más daño de tus disparos | Disparo mortal: más si el enemigo tiene tu marca |
| Mago · DPS | Chispa | Bola de fuego | Ignio: quema cada turno | Piroexplosión: detona el Ignio y lo cobra de una vez |

Todos los Básicos dan +1 de energía.

## 8. Decisiones ya cerradas por el dueño

- La Marea de sanación del Chamán escala solo con Restauración y con el número de jugadores, no con el largo de la cadena.
- La Sanación superior del Sacerdote cuesta 6, igual que todos los gastadores; la diferencia está en el efecto, no en el precio.
- Básicos seguidos = una sola marca.
- No hay tope de energía. Un gastador sin combo de 3 botones distintos pega al 80-90 %.
- La esquiva del Druida es igual al aguante del Guerrero en números.
- Tope de 5 objetivos para toda habilidad en área.
- Subir de nivel no da estadísticas por sí solo: la fuerza viene del equipo.

## 9. Pendientes del dueño (configurables, sin inventar)

| # | Pendiente | Dónde se cambia | Cómo está hoy |
|---|---|---|---|
| 1 | Los porcentajes finales del bono por marcas | `chain.mark_bonus` | 10 %, 25 % y 50 % |
| 2 | Qué habilidades de DPS no generan agro | `chain.no_threat` | Vacío: el agro solo cuenta en grupo, que todavía no existe |
| 3 | Modo híbrido: cuántas habilidades de cada rol se mezclan y el límite de botones | `chain.hybrid.max_mixed` | `null`: no se ofrece hasta que se decida |
| 4 | Si cada rol guarda sus puntos o se reparten de cero al cambiar | `chain.keep_points` | `false`: se recogen y se reparten. Hoy da igual, porque los puntos tienen un solo destino |
| 5 | Si el bono por variedad dura la pelea o es para siempre | `chain.variety.scope` | `fight`: dura la pelea. `permanent` ya funciona si se elige |
| 6 | El orden del tanque (defensa antes que agro) está en revisión | `chain.orders.tanque` | B → H2 → H1 → H3 |

Están como P-207 a P-212 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md) y como E-208 a E-213 en el [Sistema de preguntas](../00-vision/sistema-de-preguntas.md).

## 10. Cómo quedó en el juego (0.31, aplicado por Claude: D-231)

**El motor:**
- `engine/combat/chain.py` tiene las reglas de la cadena.
- `engine/combat/chain_round.py` juega la ronda: energía, marcas, premio, defenderse y el efecto de cada botón.
- Las peleas de las clases retiradas siguen en `engine/combat/engine.py`, sin cambios.

**Las clases:**
- `content/classes.yaml` tiene 12 especializaciones nuevas con `system: chain`.
- Las 46 especializaciones viejas quedan con `retired: true` y `migrate_to`. Ningún ID se borra ni se reutiliza.
- Un héroe guardado con una clase vieja pasa a la nueva al cargar, con su nivel, experiencia, equipo y monedas. Ejemplos: el Pícaro pasa a Druida · DPS; el Paladín Sagrado, a Sacerdote · Sanador.

**Pelear solo:** hoy todas las peleas son de uno contra uno.
- Lo que elige a un aliado, cura a varios o potencia al grupo cae en el héroe. Ejemplo: la Sanación en cadena de 30+30+30 cae entera en ti.
- Lo que pega a varios enemigos pega al de enfrente.
- El agro solo cuenta en grupo. En el tanque queda la parte de defensa.

**La pantalla de combate:** 6 botones como mucho (D-46).
- Los 4 de la cadena, con su costo; el Básico muestra el +1.
- 🛡️ Defenderse, que cuesta 1.
- 🎒 Mochila, con las pociones y, si se puede, 🏃 Huir.
- Arriba se ven: la energía (y el +2 del turno), las marcas, el premio que cobraría el gastador, el orden del rol con los nombres de los botones y qué sigue.

**Creación del héroe y roles:**
- Al crear el héroe se elige la clase y el primer rol.
- El segundo rol se abre al nivel 5, gratis, en 👤 Héroe → 🌟 Talentos.
- Los puntos de nivel (1 por nivel) van solos al rol activo.
- La barra es fija hasta el modo híbrido.

**Lo que agregó Claude para que el juego funcione (provisional, se ajusta en la beta):**

| Qué | Por qué |
|---|---|
| Defenderse frena la mitad del golpe (`combat.dodge_basic`) | El parche no da el número |
| El aguante o la esquiva del tanque nunca frena más del 75 % de un golpe (`chain.guard_cap`) | Para que el premio no lo haga invulnerable |
| Disparo arcano y Lentitud alargan lo activo hasta 3 turnos como mucho (`chain.extend_cap`) | Sin tope, el soporte se potenciaba para siempre |
| Los gastadores del tanque y del soporte también pegan un poco | Sin daño, pelear solo era casi imposible contra el Guardián |
| Los DPS tienen algo más de vida base que los demás | Contra el Guardián morían antes de ganar |
| Interponerse, Piel de corteza y el Escudo sagrado cubren el golpe del mismo turno, como una respuesta | Si no, un enemigo más rápido pegaba antes de que se levantaran |
| La pelea automática sigue el orden de su rol: sobrevive primero, toca el siguiente eslabón si le alcanza la energía y, si no, el Básico; remata si un golpe alcanza; el sanador sano pega | El parche no dice cómo juega sola |

**Lo que todavía no se aplica:**
- **"Subir de nivel no da estadísticas por sí solo".** El equipo de hoy solo da porcentajes chicos (una espada de nivel 60 da +28 % de ataque). Si el nivel dejara de dar vida y ataque, un héroe de nivel 20 tendría la fuerza de uno de nivel 1 contra monstruos de nivel 20. Se aplica junto con la reforma de estadísticas del equipo (D-210, D-211, E-170 a E-176). Mientras tanto, cada clase sube por nivel lo mismo que las demás de su rol.
- **Espíritu, Restauración, crítico, penetración, celeridad y versatilidad:** también llegan con esa reforma.

**Medido con `tools/sim.py`** (los objetivos de siempre: [Balance](../03-personaje/balance.md) §7):

| Prueba | Resultado |
|---|---|
| Contra cada enemigo de nivel 1 a 3 | Todas ganan el 100 % |
| Rondas por pelea | DPS unas 4, soportes unas 5, tanques unas 8, sanadores unas 8 a 9 |
| Contra el Guardián al nivel 6 | Todas entre 68 % y 90 %: tanques 84 y 90 %, sanadores 85 y 90 %, DPS 68 a 82 %, soportes 74 y 89 % |

## De dónde sale

- **El parche lo escribió el dueño** (8-oct-2026), con el mismo esqueleto para las 6 clases.
- **La idea de los botones que cargan y gastan** viene de las rotaciones de World of Warcraft: los generadores y gastadores, los puntos de combo del Pícaro, la ira del Guerrero.
- **Tejer** viene del "weaving" de los MMO de acción.
- **El tope de 5 objetivos** viene de los límites de objetivos de WoW.
