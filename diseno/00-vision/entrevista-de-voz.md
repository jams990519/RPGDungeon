# Entrevista de voz para el dueño

> **Módulo** [00 · Visión](README.md) · **Depende de:** [Preguntas abiertas](preguntas-abiertas.md), [Decisiones](decisiones.md) · **Alimenta a:** todo el diseño · **Estado:** listo para usar

**Para qué sirve.** El dueño pega el texto de abajo en un chat de voz (otro asistente), responde hablando, y trae aquí el resumen final. Cada pregunta tiene un código (E-xx) y, cuando corresponde, la pregunta abierta del diseño (P-xx) o la decisión (D-xx) que resuelve. Con el resumen se registran las decisiones y se corrige la cola de trabajo.

Todo lo que va dentro del bloque de abajo se copia tal cual.

```text
Eres mi entrevistador para el diseño de "Lost Realms", un juego de rol (RPG) por turnos y en texto que se juega en Telegram (@LostRealmsbot). Yo soy el dueño del juego. Vamos a hablar por voz: tú preguntas y yo respondo.

CÓMO TRABAJAS
1. Haz UNA pregunta a la vez, en español, corta y clara. Lee el código de la pregunta (por ejemplo "E-01"), la frase de contexto y las opciones. Di cuál es la recomendada.
2. Yo puedo responder con una opción, con mis palabras, decir "lo que recomiendes", "siguiente" o "no sé". Si mi respuesta es confusa, repítela en una frase para confirmar ("¿Entonces eliges 8 meses?") y sigue.
3. No me expliques el juego entero: con el contexto de cada pregunta basta. Si pregunto algo que no sabes, dime que lo anotas como duda.
4. Si digo "pausa", espera. Si digo "termina", ve directo al resumen.
5. No inventes respuestas. Si no respondí, escribe "sin respuesta".
6. Al terminar, escribe el RESUMEN con el formato del final, para que yo lo copie y lo pegue en otro chat.

LAS PREGUNTAS

BLOQUE 1 · DECISIONES QUE FRENAN EL TRABAJO
E-01 (P-77) Velocidad para llegar al nivel 100. Hoy, jugando todos los días con toda la energía, se tarda unos 2 años. La idea es que lo largo sea la historia y el rol, no subir lento. Opciones: unos 8 meses (recomendado), 1 año, dejar 2 años.
E-02 Peleas automáticas: con cuánta vida se retira el héroe por defecto. Con 50 % el lote se corta después de unas 4 peleas; con 30 % sigue casi entero y pierde menos del 1 % de las peleas. Opciones: 30 % (recomendado), 50 %, 70 %.
E-03 (D-117) ¿Confirmas que lo que hace largo al juego es su historia y su rol (origen del héroe, campaña por capítulos, facciones, oficios, castillo), y no un progreso lento? Sí (recomendado) / no, explícame.
E-04 (D-113) Cuando dijiste que los oficios mezclan World of Warcraft y "algo online", ¿era Albion Online? Sí / era otro juego (¿cuál?).
E-05 (P-76) Beneficios de los oficios: si alguien sube todos sus oficios, ¿se suman todos los beneficios o solo los de sus 2 mejores oficios? Opciones: se suman todos (recomendado, porque subirlos lleva mucho tiempo) / solo los 2 mejores.
E-06 La Noche de prueba (antes de castillo) pide 2 victorias de miembros distintos, así que un campamento de una sola persona no la gana. Opciones: dejarlo así, el castillo es de grupo (recomendado) / permitir que uno solo la gane.
E-07 ¿Se puede cazar dentro del territorio de tu propio campamento? Sí, para salir juntos desde casa (recomendado) / no.
E-08 ¿En qué país o zona horaria estás? Sirve para la "noche" de los Braseros y para los horarios de eventos.
E-09 (P-75) ¿Cuántas provisiones de comida se pueden comprar al mercader por semana para la despensa del campamento? Opciones: 20 (recomendado) / otro número / sin tope.

BLOQUE 2 · HISTORIA Y ROL
E-10 Tono del mundo. Opciones: oscuro y serio / épico y heroico / oscuro pero con esperanza y algo de humor (recomendado).
E-11 ¿Qué fue el Colapso, el desastre que dejó el mundo en ruinas? Dime tu idea, o "propón tú".
E-12 ¿Qué es la Lejanía, el gran misterio del mapa sin fin? Opciones: algo mágico y antiguo que se revela de a poco (recomendado) / algo divino / algo tecnológico / otra idea.
E-13 Tres facciones para empezar. Propuesta: los que quieren reconstruir el mundo, los que buscan el poder de la Lejanía y los que viven libres de lo que queda. ¿Te sirven, o qué cambias?
E-14 Orígenes para elegir al crear el héroe. Propuesta: superviviente del Colapso, hijo de artesanos, desertor, peregrino, noble caído y criado en lo salvaje. ¿Cuáles quieres? ¿Agregas alguno?
E-15 Las decisiones de la historia, ¿cambian solo tu historia o también el mundo para todos? Opciones: solo tu héroe, y algunas grandes las vota el servidor (recomendado) / solo tu héroe / todas cambian el mundo.
E-16 ¿Pueden morir personajes importantes de la historia? Sí / no / solo por decisiones del jugador.
E-17 ¿Relaciones o romance con personajes del juego? Sí / no / más adelante.
E-18 Largo de los textos de historia en Telegram. Opciones: cortos, de 2 a 4 líneas (recomendado) / medianos / largos.
E-19 (P-03) Nombres del mundo: propios y originales (recomendado) / nombres de World of Warcraft.
E-20 ¿Eventos de historia para todo el servidor, donde todos ayudan a abrir el siguiente capítulo? Sí (recomendado) / no.

BLOQUE 3 · OFICIOS Y ECONOMÍA
E-21 (P-32) Mercado entre jugadores. Opciones: un mercado en cada asentamiento, como en Albion (recomendado) / una subasta global para todos.
E-22 Impuesto del mercado (saca monedas del juego). Opciones: 5 % (recomendado) / 10 % / otro.
E-23 (P-34) Desgaste del equipo. Opciones: se gasta, se repara y un día se rompe (recomendado, como Albion) / se gasta pero nunca se rompe / no se gasta.
E-24 ¿Pedidos de fabricación: le das materiales y una paga a un artesano para que te fabrique algo? Sí (recomendado) / no.
E-25 Especializaciones de oficio: una al rango 25 y otra al 75, nunca las tres (recomendado) / otra regla.
E-26 (P-38) Fabricar: con un toque, y un minijuego opcional para sacar obras maestras (recomendado) / siempre con minijuego / siempre con un toque.
E-27 (P-39) ¿Recursos con calidad según el lugar donde salen? Sí, más adelante (recomendado) / no.
E-28 Hay 26 oficios previstos (leñador, minero, herbolario, cazador, pescador, agricultor, ganadero, explorador; refinados; carpintería, herrería, peletería, sastrería, alquimia, joyería, encantamiento, inscripción, ingeniería, medicina, cocina, construcción; comercio). ¿Agregas o quitas alguno?
E-29 (P-74) Una zona muy recolectada se agota. ¿Cómo vuelve antes? Opciones: el herbolario o el agricultor siembra con semillas (recomendado) / vuelve sola con el tiempo y nada más / otra idea.
E-30 (P-70) ¿Los oficios que no usas se olvidan poco a poco? No (recomendado) / sí.

BLOQUE 4 · COMBATE Y RIESGO
E-31 (P-26) ¿Modo de muerte permanente opcional, para quien quiere riesgo, con premios solo de prestigio? Sí, opcional (recomendado) / no.
E-32 (P-27) Pelear contra otros jugadores (PvP). Opciones: solo en zonas marcadas, donde puedes perder parte de lo que llevas (recomendado) / solo en arena, sin perder nada / no quiero PvP.
E-33 (P-28) Quien ataca a otros jugadores queda marcado (verde, naranja, rojo) y los demás pueden cazarlo. Sí (recomendado) / no.
E-34 Combate en grupo: mazmorras, bandas y Guardianes entre varios, a veces con hora fija. Sí (recomendado) / no / solo sin horarios.
E-35 (P-12) Hay 15 clases con 3 especializaciones cada una. ¿Está bien o agregas alguna clase?
E-36 (P-20 a P-22) Heridas y enfermedades. Opciones: capa simple, que se cura en horas y nunca deja al héroe inútil (recomendado) / realistas y duras / sin heridas ni enfermedades.
E-37 Dificultad general. Opciones: relajada / media, difícil pero justa (recomendado) / difícil.

BLOQUE 5 · CAMPAMENTOS Y CASTILLOS
E-38 Oleadas de enemigos contra tu campamento cada 7 días. ¿Está bien? Sí (recomendado) / más seguido / menos seguido.
E-39 (P-10, P-54) ¿Debe haber un tope de castillos en el servidor? Opciones: sin tope, los campamentos que crezcan llegan (recomendado) / con tope / otra idea.
E-40 (P-31) Guerra entre castillos. Opciones: sí, más adelante, en días y horas fijas (recomendado) / sí, en cualquier momento / no.
E-41 ¿Quién manda en un castillo? Opciones: el fundador con un consejo elegido por los miembros (recomendado) / solo el fundador / votación para todo.
E-42 (P-43) ¿Casa propia para cada jugador? Sí, temprano (recomendado) / más adelante / no.
E-43 (P-52) ¿Lo construido se puede atacar con el dueño desconectado? Opciones: sí, pero lo defienden sus defensas automáticas (recomendado) / no / sí, sin defensas.

BLOQUE 6 · COMUNIDAD, PLATAFORMA Y DINERO
E-44 (P-04) Idiomas. Opciones: solo español al principio (recomendado) / español e inglés desde ya.
E-45 (P-05) ¿Cuántos jugadores esperas el primer año?
E-46 (P-06) ¿Quieres avisar a los jugadores de TowerWars sobre Lost Realms? Ojo: TowerWars no se toca; el aviso lo publicarías tú. Sí / no.
E-47 (P-72) Vender diamantes con Telegram Stars (los diamantes solo compran cosméticos y aceleradores). Opciones: al terminar la beta (recomendado) / ya / nunca.
E-48 (P-64) ¿Se cobra algo durante la beta? No (recomendado) / sí.
E-49 (P-65, P-66) El acelerador de experiencia hoy da +50 % durante 7 días. ¿Está bien? ¿También debería subir el botín de equipo? Recomendado: está bien, y solo experiencia y recursos, nunca equipo.
E-50 (P-58, P-61) Versión web y app. Opciones: la web después de la beta, y la app como web instalable en el teléfono (recomendado) / todo ya / solo Telegram.
E-51 (P-42) ¿Grupos de Telegram oficiales por castillo y por región? Sí (recomendado) / no.

BLOQUE 7 · PRIORIDADES E IDEAS
E-52 ¿Qué quieres primero de lo que falta? Opciones: historia y rol / explorador y campamentos enemigos / más oficios (cocina, pesca, construcción, encantamiento) / mercado entre jugadores / misiones y encargos / combate en grupo. Ordénalos.
E-53 ¿Algo de lo que ya está en el juego que no te guste o quieras cambiar?
E-54 ¿Alguna idea nueva que quieras agregar?

FORMATO DEL RESUMEN FINAL (escríbelo así, sin nada más antes ni después):
RESPUESTAS LOST REALMS · ENTREVISTA DE VOZ
E-01: [opción elegida o respuesta corta] | [detalle o condición, si dijo algo más]
E-02: ...
(una línea por pregunta, de E-01 a E-54, en orden; "sin respuesta" si se saltó; "recomendación" si dijo "lo que recomiendes")
DUDAS: [lo que preguntó y no supiste responder]
IDEAS SUELTAS: [cualquier idea que dijo fuera de las preguntas]
```

**Cuando vuelva el resumen:** cada línea se registra como decisión confirmada (D-xx) o se marca la P-xx como decidida. Las que digan "recomendación" se toman con el número recomendado. Después se ajustan la cola de trabajo y los números del juego.

## Estado de las respuestas

**1-oct-2026, primera tanda (E-01 a E-43).** Registradas como decisiones confirmadas **D-118 a D-160** en [Decisiones](decisiones.md), y 22 preguntas abiertas quedaron decididas en [Preguntas abiertas](preguntas-abiertas.md). Las que cambiaban números del juego entraron en la **0.22.1**: oleadas 3 veces por semana (D-154), retirada automática al 30 % (D-119), tope de 20 provisiones por semana (D-125) y la Lejanía sin misterio en los textos (D-128).

**Sin respuesta todavía:**
- **E-03** (si lo largo es la historia y no un progreso lento): D-117 sigue provisional. El ritmo al nivel 100 no cambia (D-118).
- **El tono de E-10:** sigue la propuesta (D-161, provisional).
- **E-44 a E-54** (bloques 6 y 7: idiomas, jugadores esperados, aviso a TowerWars, diamantes, cobro en la beta, acelerador, web y app, grupos de Telegram, prioridades, qué no te gusta e ideas nuevas).

Todas van, junto con las dudas nuevas, en la **segunda tanda** de abajo.

## Segunda tanda (1-oct-2026)

> ⚠️ **La versión vigente está en el [Sistema de preguntas](sistema-de-preguntas.md)**, que junta esta tanda con las preguntas viejas del diseño y las de antes de la beta. El texto de abajo queda como historia.

**Para qué sirve.** Junta en una sola charla lo que quedó sin responder (E-03, el tono de E-10 y los bloques 6 y 7: E-44 a E-54) y las dudas nuevas que salieron de la primera tanda (**E-55 a E-82**, registradas como P-78 a P-105 en [Preguntas abiertas](preguntas-abiertas.md)), más lo que quedó pendiente de la ampliación de diseño (**E-83 a E-91**, P-106 a P-114). E-73 y E-77 se quitaron porque la ampliación las respondió (D-168 y D-166), y E-58 se cambió a 10 etapas. **Versión final (1-oct-2026):** se sumaron 6 dudas nuevas (**E-92 a E-97**, P-115 a P-120), E-52 tiene las prioridades de hoy y el orden va de lo que frena trabajo a lo que puede esperar. Las preguntas que frenan trabajo son las de los bloques C, D y E: deciden cómo se programan el asentamiento por escalones, las razas, el día y la noche, y la economía entre jugadores.

Todo lo que va dentro del bloque de abajo se copia tal cual.

```text
Eres mi entrevistador para el diseño de "Lost Realms", un juego de rol (RPG) por turnos y en texto que se juega en Telegram (@LostRealmsbot). Yo soy el dueño del juego. Esta es la segunda parte de la entrevista: las preguntas que quedaron sin responder y todas las dudas que salieron de mis respuestas y de la ampliación de diseño. Van primero las que frenan trabajo; si me canso, digo "termina" y se guarda lo respondido. Vamos a hablar por voz: tú preguntas y yo respondo.

CÓMO TRABAJAS
1. Haz UNA pregunta a la vez, en español, corta y clara. Lee el código de la pregunta (por ejemplo "E-55"), la frase de contexto y las opciones. Di cuál es la recomendada.
2. Yo puedo responder con una opción, con mis palabras, decir "lo que recomiendes", "siguiente" o "no sé". Si mi respuesta es confusa, repítela en una frase para confirmar ("¿Entonces eliges 15 en la beta?") y sigue.
3. No me expliques el juego entero: con el contexto de cada pregunta basta. Si pregunto algo que no sabes, dime que lo anotas como duda.
4. Si digo "pausa", espera. Si digo "termina", ve directo al resumen.
5. No inventes respuestas. Si no respondí, escribe "sin respuesta".
6. Al terminar, escribe el RESUMEN con el formato del final, para que yo lo copie y lo pegue en otro chat.

LAS PREGUNTAS

BLOQUE A · LO QUE QUEDÓ SIN RESPONDER Y TUS PRIORIDADES
E-03 (D-117) Elegiste dejar el nivel 100 en unos 2 años. ¿Entonces lo que hace largo al juego son las dos cosas: subir de nivel y también la historia, el rol, los oficios y el castillo? Sí, las dos (recomendado) / solo la historia y el rol, y que subir sea más rápido.
E-10 Tono del mundo. Opciones: oscuro y serio / épico y heroico / oscuro pero con esperanza y algo de humor (recomendado).
E-52 ¿Qué quieres primero de lo que falta? Ordena: asentamiento por etapas y castillo / razas y facciones nuevas / mazmorras de grupo y jefes de mundo / subasta entre jugadores y desgaste del equipo / enfermedades, médico y alquimista / PvP y bandidos / día, tarde y noche / eventos, temporadas y logros.

BLOQUE B · ASENTAMIENTO, CASTILLO Y HORARIOS
E-55 (P-78) Mínimo de miembros para pedir castillo. Dijiste de 40 a 50, pero en la beta habrá pocos jugadores. Opciones: 15 durante la beta y 40 desde el lanzamiento (recomendado) / 40 desde ya / otro número.
E-56 (P-79) Para aprobar el castillo, ¿cuántas oleadas seguidas hay que defender y cuántas victorias de cuántos miembros pide la Noche de prueba? Recomendado: 6 oleadas en dos semanas, ganando al menos 4, y una Noche de prueba con 10 victorias de al menos 5 miembros distintos. ¿Está bien o cambias los números?
E-57 (P-80) La casa del inicio: ¿es el primer escalón del asentamiento (la casa crece y se vuelve campamento, aldea, ciudad...) o cada jugador tiene además su propia casa dentro del asentamiento? Opciones: la casa es el primer escalón, compartido por 3 a 5 jugadores (recomendado) / cada uno tiene su casa aparte / las dos cosas.
E-58 (P-81) Etapas del asentamiento: quieres más de 7 (Ashes of Creation tiene 7). Propongo 10: casa, campamento, aldea, pueblo, villa, ciudad, fortaleza, castillo, ciudadela y reino; las primeras rápidas y las últimas lentas. ¿Te sirven 10 y esos nombres, o cuántas y cuáles?
E-59 (P-82) Monarquía y votación: si en el castillo todo se vota, ¿qué decide solo el monarca? Recomendado: el fundador es el monarca y decide el nombre, la bandera, declarar la guerra y aceptar o echar miembros; todo lo demás se vota. ¿Así u otra idea?
E-60 (P-83) Las oleadas contra los campamentos: ¿en días y horas fijas iguales para todos (por ejemplo lunes, miércoles y viernes a las 8 de la noche) o cada campamento con su propio ritmo desde que se fundó? Opciones: días y horas fijas, avisadas (recomendado, como pediste para combates y eventos) / cada uno su ritmo.
E-61 (P-84) Hora de referencia para los eventos fijos (oleadas, asedios, jefes de mundo). Recomiendo la noche de América, de 7 a 11 de la noche en hora de Colombia, Perú o Ecuador (UTC−5). ¿Te sirve u otra?
E-62 (P-85) Guerra de castillos: ¿quién puede atacar a quién? Recomendado: solo los castillos declaran la guerra; pueden atacar desde aldea para arriba, y un asentamiento recién fundado tiene 2 semanas de protección. Otras opciones: cualquiera contra cualquiera / solo castillo contra castillo.

BLOQUE C · DÍA Y NOCHE, RAZAS Y FACCIONES
E-63 (P-86) Día, tarde y noche: ¿cuánto dura un día del mundo? Si dura justo un día real, quien juega siempre a la misma hora ve siempre la misma franja. Opciones: 4 días reales (recomendado: cada franja dura unas 32 horas y todos ven las tres) / 1 día real / otro.
E-64 (P-87) ¿Las franjas cambian también el peligro? Por ejemplo, de noche salen enemigos más fuertes con mejor botín. Sí (recomendado) / no, solo cambian los recursos.
E-65 (P-88) Razas: ¿clásicas de la fantasía con nombres e historia propios de este mundo (humanos, elfos, enanos, orcos, medianos, bestiales...) o razas inventadas desde cero? Clásicas con historia propia (recomendado) / inventadas.
E-66 (P-89) ¿Cuántas razas al empezar, y la raza limita qué clases puedes elegir? Recomendado: 6 razas, todas pueden ser cualquier clase y la raza solo da un beneficio chico de oficio y de arma / con límites de clase como en World of Warcraft.
E-67 (P-90) Los héroes que ya existen, ¿eligen raza una vez gratis, como pasó con el origen? Sí (recomendado) / quedan como humanos.
E-68 (P-91) ¿La facción de los ladrones es la casa de los bandidos (los que atacan jugadores y transportes)? Sí (recomendado) / no, son cosas separadas.

BLOQUE D · ECONOMÍA Y OFICIOS
E-69 (P-92) Subasta global con transportistas: ¿dónde recibes lo que compras y cuánto tarda? Recomendado: llega a tu asentamiento o al Claro, tarda según la distancia (de minutos a unas horas) y puedes pagar más para que llegue antes. Otras: llega al instante / otra idea.
E-70 (P-93) Desgaste generoso del equipo. Recomendado: una pieza aguanta unas 3 semanas jugando todos los días antes de pedir reparación; cada reparación le baja un poco el máximo, y tras unas 5 reparaciones se rompe del todo (unos 4 meses de vida). ¿Bien, más o menos?
E-71 (P-94) ¿Las obras maestras firmadas también se gastan? Recomendado: sí, pero aguantan el doble / no se gastan nunca / igual que las normales.
E-72 (P-95) Hoy vender al mercader una obra maestra deja un poco más (un 3,7 %) de lo que valen sus materiales. ¿Lo bajo para que fabricar y vender al mercader no sea negocio? Bajarlo (recomendado: el dinero de verdad debe venir de venderle a otros jugadores) / dejarlo así.
E-74 (P-97) Tope diario de recursos en tu territorio. Recomendado: cada zona da un total por día; pasado ese total, rinde la mitad, y por eso conviene salir a los alrededores. ¿Así?

BLOQUE E · MAZMORRAS, EVENTOS, ENFERMEDADES Y FUSIÓN
E-83 (P-106) Arena: ¿una arena para pelear contra otros jugadores sin perder nada, desde el principio (también en la beta)? Sí (recomendado: se practica sin riesgo y ayuda a balancear las clases) / no / más adelante.
E-84 (P-107) Eventos y temporadas. Recomendado: un evento corto cada mes (unas 2 semanas, con su historia y su botín) y temporadas de 3 meses con premios cosméticos y una tabla de clasificación; el progreso del héroe nunca se borra. ¿Así u otra idea?
E-85 (P-108) Jefes de mundo. Recomendado: aparecen en lugares del mapa a horas avisadas (la hora de referencia de E-61) para muchos jugadores a la vez, y el botín se reparte según lo que hizo cada uno en su rol (daño, tanque o curación). ¿Así?
E-86 (P-109) Logros y rangos. Recomendado: logros de todo (combate, oficios, exploración, historia, campamento) que dan títulos, marcos y emblemas sin poder de combate, y rangos por temporada. ¿Así?
E-87 (P-110) PvP dentro de las mazmorras: no, las mazmorras son siempre contra monstruos (recomendado) / sí, en algunas mazmorras marcadas / sí, en todas.
E-88 (P-111) Botín no cortado a tu medida: hoy el 70 % de las piezas que caen son de tu tipo. Recomendado: bajarlo al 40 % cuando exista la subasta, para que el resto lo vendas a quien lo necesite / bajarlo ya / otro número.
E-89 (P-112) Fusión de un campamento chico con un castillo. Recomendado: se anuncia con 7 días de aviso; lo que muden los miembros en esos días se conserva, y el castillo recibe la mitad de lo que costaron las obras del campamento; lo que no se mudó se pierde. ¿Así?
E-90 (P-113) Vasallos, como en Ashes of Creation: ¿los asentamientos grandes pueden tener a los chicos como vasallos? Más adelante, junto con la guerra de castillos (recomendado) / no / sí, desde ya.
E-91 (P-114) Enfermedades: ¿desde cuándo aparecen? Recomendado: las primeras, leves, desde el nivel 15 y lejos del Claro; las graves, y las que siguen después de morir, desde el nivel 40. ¿Así?

BLOQUE F · DUDAS NUEVAS
E-92 (P-115) Cuando el campamento defiende bien una oleada, hoy igual pierde 1 punto de defensa (y 2 si la pierde). Con 3 oleadas por semana el daño se junta rápido. Recomendado: defenderla bien no daña nada; solo dañan las que se pierden / dejarlo como está.
E-93 (P-116) Beneficios de oficio del campamento (cocina, pesca, cantería, construcción): hoy cuenta el mejor miembro del grupo en cada oficio. Recomendado: así, el mejor del grupo / se suman los de varios miembros.
E-94 (P-117) Mazmorras de grupo: dijiste que tanque y curador necesitan recompensa propia. Recomendado: todos ganan lo mismo por terminar, y el tanque y el curador se llevan además un cofre extra, porque son los roles que menos se eligen. ¿Así u otra forma?
E-95 (P-118) ¿Cómo se arma un grupo? Recomendado: con los que están en tu misma zona, con un botón para formar grupo y otro para sumarse (como dijiste) / también invitando por nombre a alguien que está lejos.
E-96 (P-119) Los nodos que mejora el carpintero: ¿para quién son? Recomendado: en zonas libres, la mejora sirve a todos; dentro del territorio de un campamento, solo a sus miembros. Duran unos días y hay que mantenerlas. ¿Así?
E-97 (P-120) La información de enfermedades que cazadores e investigadores les pasan a médicos y alquimistas: ¿es un objeto que se puede vender? Recomendado: sí, un informe que se consigue al encontrar la enfermedad y que se vende o se regala / no, se comparte gratis y sin objeto.

BLOQUE G · PVP Y NODOS
E-75 (P-98) ¿Cómo se marcan las zonas de PvP? Recomendado: según la distancia al Claro: cerca, seguras; a media distancia se pierde el 10 % de la mochila; lejos, el 20 %; muy lejos, el 40 %. Los asentamientos siempre seguros. ¿Así u otra forma?
E-76 (P-99) ¿Cuándo entra el PvP? Después de la beta, cuando haya suficientes jugadores (recomendado) / ya en la beta.
E-78 (P-101) Los nodos especiales que descubren los expertos: ¿de quién hay que defenderlos? De monstruos que aparecen (recomendado al principio) / de otros jugadores, cuando haya PvP / de los dos.

BLOQUE H · DETALLES DE LO QUE YA ESTÁ EN EL JUEGO
E-79 (P-102) Explorador: los que ya exploraban antes de que existiera el oficio, ¿reciben experiencia de Explorador por lo que exploraron? Sí, una parte (recomendado) / no, todos empiezan desde cero.
E-80 (P-103) Si fundas o agrandas tu asentamiento donde hay un campamento enemigo, ¿se prohíbe hasta destruirlo? Sí (recomendado) / no, el campamento enemigo desaparece.
E-81 (P-104) Los jefes de los campamentos enemigos lejanos, ¿piden grupo? Sí, desde cierta distancia (recomendado) / no, siempre se pueden hacer solos.
E-82 (P-105) Cambiar de especialización de oficio: dijiste que se puede pagando y empezando de cero en la nueva. Lo dejé así: elegir la primera y la segunda es gratis; cambiar cuesta 1 de plata más 20 de bronce por rango (unas 6 de plata al rango 25 y 21 al rango 100), y lo aprendido en la vieja queda guardado por si vuelves. ¿Está bien o lo cambias?

BLOQUE I · COMUNIDAD, PLATAFORMA Y DINERO
E-44 (P-04) Idiomas. Opciones: solo español al principio (recomendado) / español e inglés desde ya.
E-45 (P-05) ¿Cuántos jugadores esperas el primer año?
E-46 (P-06) ¿Quieres avisar a los jugadores de TowerWars sobre Lost Realms? Ojo: TowerWars no se toca; el aviso lo publicarías tú. Sí / no.
E-47 (P-72) Vender diamantes con Telegram Stars (los diamantes solo compran cosméticos y aceleradores). Opciones: al terminar la beta (recomendado) / ya / nunca.
E-48 (P-64) ¿Se cobra algo durante la beta? No (recomendado) / sí.
E-49 (P-65, P-66) El acelerador de experiencia hoy da +50 % durante 7 días. ¿Está bien? ¿También debería subir el botín de equipo? Recomendado: está bien, y solo experiencia y recursos, nunca equipo.
E-50 (P-58, P-61) Versión web y app. Opciones: la web después de la beta, y la app como web instalable en el teléfono (recomendado) / todo ya / solo Telegram.
E-51 (P-42) ¿Grupos de Telegram oficiales por castillo y por región? Sí (recomendado) / no.
E-53 ¿Algo de lo que ya está en el juego que no te guste o quieras cambiar?
E-54 ¿Alguna idea nueva que quieras agregar?

FORMATO DEL RESUMEN FINAL (escríbelo así, sin nada más antes ni después):
RESPUESTAS LOST REALMS · ENTREVISTA DE VOZ · SEGUNDA PARTE
E-03: [opción elegida o respuesta corta] | [detalle o condición, si dijo algo más]
E-10: ...
(una línea por pregunta, en este orden: E-03, E-10, E-52, E-55, E-56, E-57, E-58, E-59, E-60, E-61, E-62, E-63, E-64, E-65, E-66, E-67, E-68, E-69, E-70, E-71, E-72, E-74, E-83, E-84, E-85, E-86, E-87, E-88, E-89, E-90, E-91, E-92, E-93, E-94, E-95, E-96, E-97, E-75, E-76, E-78, E-79, E-80, E-81, E-82, E-44, E-45, E-46, E-47, E-48, E-49, E-50, E-51, E-53, E-54; "sin respuesta" si se saltó; "recomendación" si dijo "lo que recomiendes")
DUDAS: [lo que preguntó y no supiste responder]
IDEAS SUELTAS: [cualquier idea que dijo fuera de las preguntas]
```

**Cuando vuelva el resumen:** igual que la primera tanda: cada línea es una decisión confirmada (D-xx) y su P-xx se marca decidida. Las que digan "recomendación" se toman con lo recomendado.

## Ampliación de diseño (sesión del dueño después de la entrevista, 1-oct-2026)

El dueño trajo este resumen de otra charla. Quedó registrado como decisiones confirmadas **D-164 a D-173**; sus pendientes pasaron a la segunda tanda (E-83 a E-91, y E-58 para el número de etapas).

```text
LOST REALMS · AMPLIACIÓN DE DISEÑO (sesión posterior a la entrevista E-01 a E-54)

MAZMORRAS
- Estructura fija: misma cantidad de enemigos y de jefes en cada entrada.
- Se reinician a diario. Cambia la facción que la rellena, el jefe concreto, el camino y el botín (hoy duendes, mañana slimes, pasado dragones).
- Todo tipo de enemigo tiene su propio jefe (lobos, osos, todo). Ninguna mazmorra está atada a una temática.
- La misma mazmorra se corre con 5, 10, 20 o más de 25 jugadores. A mayor grupo, mayor dificultad y mayor recompensa.
- Un jugador solo en la zona puede ser invitado o unirse a otros que estén ahí.
- Recordatorio de diseño: si solo se premia el daño, nadie quiere ser tanque ni curador. Esos roles necesitan recompensa propia.

BOTÍN
- Variable, no cortado a la medida del jugador. Caen piezas y materiales de otras clases y oficios para venderlos a quien los necesite. Alimenta el mercado.

ENFERMEDADES Y ESTADOS
- Los enemigos transmiten enfermedades y efectos.
- Estados tipo putrefacción (estilo Dark Souls) que se agravan con el tiempo y obligan a ir al médico. No se curan solos.
- Los estados son acumulables (ej. putrefacción + pierna perdida por una herida a largo plazo, a la vez).
- Morir por enfermedad cuesta las 4 horas normales, pero hay enfermedades que NO se quitan al morir: se resucita infectado hasta ser curado.
- No entran al principio del juego (sería injusto). Aparecen progresivamente, cada vez más complicadas.

MÉDICO Y ALQUIMISTA
- Médico: lo físico (heridas, fracturas, partes del cuerpo perdidas).
- Alquimista: lo químico (venenos, enfermedades, putrefacción) con pociones y antídotos.
- Ninguno cubre lo del otro.
- Aprenden por dos vías: práctica con pacientes, e información que les pasan cazadores e investigadores sobre las enfermedades que encontraron. En niveles avanzados se necesitan ambas.
- El peso de estos oficios depende de la variedad de enfermedades, problemas y situaciones que existan.

PRINCIPIO GENERAL DE PROFESIONES
- El modelo médico/alquimista se aplica a TODOS los oficios: cada uno cubre un pedazo, ninguno cubre todo, siempre se depende de otro jugador.
- Los oficios se encadenan: el sastre básico trabaja con lo que consigue, pero para escalar necesita fibras y pieles de agricultura y ganadería. Igual con el resto.
- Carpintero: fabrica y mejora herramientas e instrumentos de farmeo, y es el encargado de subir el nivel de farmeo de los propios nodos.

MATERIALES
- Fuentes exclusivas: unos solo de ganadería o agricultura, otros solo de investigación, otros solo de matar cierto tipo de monstruo, otros solo de eventos. También caen en el entorno exterior cazando y recolectando.
- Cada vía tiene su beneficio propio; ninguna reemplaza a otra.
- En lo complicado, cada vía necesita de una o dos vías más. Lo básico se hace solo.
- También hay tareas básicas que cualquiera puede hacer pero que se comercian porque a otro le conviene comprarlas. Ingreso constante para jugadores nuevos.

JUGADOR EN SOLITARIO (las tres vías)
- Mazmorras pequeñas para uno solo con recompensa modesta (modelo delves de Elder Scrolls Online).
- Mazmorras profundas de pisos donde se baja hasta donde se aguante (modelo Deep Dungeon de Final Fantasy XIV).
- Camino de profesiones: cazar, recolectar, investigar, abastecer y comerciar sin pelear.

MAPA Y NODOS
- Mapa infinito: al avanzar en cualquier eje aparece contenido distinto.
- En cada tramo se muestran 2-3 iconos de nodos y 1-2 mazmorras. Se sabe que hay algo, pero no qué es hasta ir a investigar.
- Los nodos cambian y se mejoran con las profesiones.
- Los monstruos se restablecen o incluso suben de dificultad.

EXPLORADOR
- Aprende sigilo y habilidades para obtener información de un lugar antes de llegar.
- Gana experiencia y recompensas propias por el reconocimiento.

ETAPAS DE ASENTAMIENTO
- Referencia: Ashes of Creation tiene 7 etapas (Yermo, Expedición, Campamento, Aldea, Pueblo, Ciudad, Metrópolis). La Aldea es el gran salto (edificios permanentes, alcalde, casas, edificio único por tipo de nodo: militar, económico, divino o científico). Metrópolis: máximo 5 por servidor, abre mazmorras raras y final de juego. Los grandes someten a los pequeños como vasallos.
- Jams quiere MÁS de 7 para que el progreso se sienta más fluido. Propuesta: 10 etapas (POR CONFIRMAR).
- Las primeras etapas rápidas; luego cada vez más lentas.
- Cada etapa sube capacidad de aldeanos, casillas del mapa y permisos. Contenido nuevo (mercado, templo, taller avanzado) solo cada 2-3 etapas.
- Para avanzar de etapa hay que tener construidas ciertas estructuras.
- Las etapas tempranas son jugables para grupos pequeños que no caben en un castillo.
- Fusión: un grupo pequeño puede desmantelar su campamento y unirse a un castillo, aportando parte de sus recursos a la estructura nueva. Hay que mover las cosas con anticipación; lo que no se traslade a tiempo se pierde y se destruye.
- Los campamentos pequeños también pueden ser atacados (aplican las reglas de asedio ya definidas: aviso anticipado y mínimo de atacantes según tamaño).

PENDIENTES
- Confirmar número exacto de etapas de asentamiento.
- E-03 sigue sin respuesta.
- Arena sin pérdidas desde el principio (E-32): sin respuesta.
- Temas sin tocar: eventos y temporadas, world bosses, logros y rangos, PvP en mazmorras.
```

## Ideas sueltas del mapa y la interfaz (1-oct-2026)

El dueño mandó estas ideas por el chat. Quedaron registradas como decisiones confirmadas **D-178 a D-181**; cómo se aplican, en D-182 (provisional). Sus dudas pasaron al [Sistema de preguntas](sistema-de-preguntas.md) (E-123 a E-126).

```text
LOST REALMS · IDEAS SUELTAS (mapa e interfaz)

MENÚ DE OPCIONES
- Cada interruptor muestra una palomita VERDE cuando está activo y una palomita GRIS cuando está desactivado.

MAPA · TERRENOS Y RECURSOS
- El mapa se define automáticamente con colores por tipo de terreno (ej. verde = pradera o campo normal). Se pueden agregar todos los colores que hagan falta.
- Cada tipo de terreno tiene un catálogo de 10 a 15 recursos posibles.
- Cada casilla o zona solo trae una parte de ese catálogo (ej. 4 o 6 de los 15), en cantidades variables.
- El color no garantiza un recurso concreto: ver verde no significa que siempre haya madera o semillas. Hay que ir a investigar.

MAPA · ICONOS
- Icono de CUEVA: marca dónde hay una mazmorra. Dos o tres por zona, a distintas distancias y posiciones.
- Icono propio para los CAMPAMENTOS DE MONSTRUOS.
- NODOS DE RECURSOS: colocados al azar con un símbolo genérico. Solo al llegar se descubre qué tipo de nodo principal es.
```

## Pedido del dueño: la historia como camino guiado (2-oct-2026)

El dueño lo dijo por voz en el chat. Quedó registrado como decisiones confirmadas **D-190** (camino guiado, sin la opción 📖 Historia) y **D-191** (campamento, entrenador, ❓ Dudas y héroe); sus dudas pasaron al [Sistema de preguntas](sistema-de-preguntas.md) (E-129 a E-133). Transcripción tal cual llegó (con los cortes de la voz):

```text
Ok, la historia la vas a definir de otra manera. Vas a botar, borrar esa opción. Y vas a ir a medida que va, vas a mandarlo a hacer una opción, una acción, cada vez que encuentra algo nuevo. O sea, lo primero que lo vas a mandar es a mover en el mapa. Ahí le vas a dar un pequeño, una pequeña introducción de cómo te puedes mover el mapa, qué tiempo dura, qué tipos de mapa hay y todo lo demás. [...] Vas a escoger tu jugador, demás y demás. Le vas a poner la clase, le vas a poner el nombre. Y aún no escojas la raza porque eso no está definido. Luego, lo segundo que vas a ver, ¿dónde estás? Estás en el primer lugar donde está, explorar en el mapa, mapa, lugares y la primera zona donde sales, donde está la antorcha, por ejemplo. [...] Lo primero que te va a decir: ok, has llegado a un lugar así, así, así; hay diferentes tipos de terreno en los alrededores. Y deberás moverte antes de llegar a esos lugares para investigar, número uno, y número dos, deberás investigar, hacer misiones y demás. Entonces lo primero que vas a hacer es mandarlo a moverse en cualquiera de las casillas. Cuando regresa el jugador, puede encontrarse con mobs. Ese movimiento, recuerda que no gasta energía los movimientos entre zonas pero gasta tiempo. Una vez llega a la zona lo vas a mandar primero a hacer una exploración, luego una recolección, luego una caza. Una vez ha hecho eso ya has avanzado un poquitico [...] luego vas a mandarlo al mapa y vas a ir mostrándole toda la información que puedes mencionarle; luego vas a ir al campamento, lo vas a mandar a regresar al campamento. Esta opción del campamento no me gusta: el campamento debería tener la opción de cocinar, investigar, craftear y cosas así, lo que debería estar en orden. Luego tienes el botón del héroe con todos los talentos, mochila, salud y todo lo demás. Ahora, cuando le damos en campamento, van a salir también un botón para preguntas, por ejemplo, que va a ir aclarando absolutamente todas las dudas que tengan los jugadores; le vas a poner dudas, que va a ser una IA que cuando tú le menciones algo te va a mostrar una serie de dudas o una serie de preguntas que ya van a estar prerrespondidas; por ejemplo, puedo utilizar un código que llame a la respuesta de cierta pregunta y así sucesivamente. Ahora, en el campamento, número uno vamos a hacer lo que no está en héroe; número dos vas a poder escoger tutor, por ejemplo, o entrenador, donde vas a empezar a presentarle, cuando hayas regresado, las profesiones y todo lo demás.
Y a medida que vas desbloqueando, por ejemplo, vas a comentarle al jugador en parte del tutorial: ahora aquí está el botón de mejora. Una vez estás en el campamento, que creas un campamento: no vas a darle un tutorial de cómo crear un campamento; primero tiene que moverse a otra zona que no es la antorcha principal. Una vez que lo has movido a otra zona, le vas a explicar o lo vas a mandar a hacer varios movimientos, uno o dos movimientos, y vas a decirle: mira, has encontrado un buen lugar para crear un campamento propio, y le vas a permitir a ese jugador darle nombre al campamento. Una vez ha creado el campamento le vas a dar un pequeño tutorial: mira, estas son todas las cosas que puedes hacer aquí: tienes un mercader, tienes un entrenador, un máster que te va a enseñar profesiones, y ahí empiezas a mostrarle lo que son las profesiones. Pero a medida que el jugador va desbloqueando contenido es que vas a irle dando los tutoriales, no todo de golpe. Entonces obviamente vas a comentarle al jugador que a medida que va avanzando en el juego va a ir aprendiendo profesiones de más y de más. Quiero que te fijes en el formato de Tower Wars actual, que está bien ampliado, detallado y separado. No es el mejor juego para guiarse, pero el sistema está bueno.
```

## 2-oct-2026 · Decisiones de diseño (continuación)

El dueño pegó este bloque en el chat, junto con dos preguntas. Quedó registrado como decisiones confirmadas **D-196 a D-205** en [Decisiones](decisiones.md) (D-205 sale de la segunda pregunta: comen los aldeanos, no los jugadores). Las dos respuestas de Claude quedaron como provisionales: **D-206** (armaduras) y **D-207** (comida de los aldeanos). Los pendientes de abajo y la confirmación de D-206 y D-207 pasaron al [Sistema de preguntas](sistema-de-preguntas.md), tanda 1, bloque A3 (**E-161 a E-169**). El detalle de nodos, caravanas, aldeanos y comida está en [Caravanas y aldeanos](../02-mundo/caravanas-y-aldeanos.md). Texto tal cual llegó:

```text
DECISIONES DE DISEÑO · LOST REALMS (continuación)
1. ENERGÍA
- Una sola barra de energía compartida para todas las acciones (recolectar, combatir, escoltar). Así no se pueden hacer varias cosas a la vez.
- Para empezar una acción, el jugador debe tener de entrada toda la energía que esa acción requiere. Si no le alcanza, no puede empezar. Nadie se queda a medias.
2. MOVIMIENTO
- Moverse por el mapa NO cuesta energía; cuesta TIEMPO: 1 minuto real por cuadro (10 cuadros = 10 minutos).
- Farmear SÍ cuesta energía. El costo depende del tamaño del nodo.
- Regla: desplazarse cuesta tiempo; trabajar (farmear solo o en caravana) cuesta energía.
3. GEMAS
- El Joyero refina las gemas a partir de los recursos de minería.
- El Minero alimenta dos cadenas: metal para el Herrero y mena para que el Joyero refine gemas.
4. RANURAS
- Pueden llevar ranura TODAS las piezas de armadura y las armas.
- NUNCA llevan ranura los anillos, collares, amuletos ni ningún accesorio. Su valor está en los bonos con que los crea el Joyero o el Alquimista.
- Se mantiene: la ranura solo aparece en piezas de buena calidad; las comunes no llevan.
5. ETAPAS DEL ASENTAMIENTO
- Número de etapas EN REVISIÓN (puede ser más o menos de 10). Se definirá según la cantidad de jugadores por asentamiento.
6. NODOS INTERNOS Y EXTERNOS
- Nodos internos: dentro del territorio de la civilización. Se mejoran directamente y los farmean los miembros.
- Nodos externos: fuera del territorio. Las mejoras de nodo aplican aquí. No se explotan directamente; requieren caravana.
7. CARAVANAS (farmeo grupal)
- La caravana es un farmeo grupal hacia un nodo externo. La civilización envía aldeanos (mano de obra que recolecta), y los jugadores deben escoltarla físicamente durante todo el trayecto.
- Requisito: campamento mejorado. Se desbloquea a partir de la 2.ª o 3.ª mejora del asentamiento.
- La cantidad de caravanas simultáneas sube con las etapas, porque a más etapas caben más jugadores disponibles para escoltar.
- Las caravanas tienen distintos tamaños. Un nodo se puede traer en un solo viaje grande o en varios viajes más pequeños.
- A mayor tamaño de caravana (más capacidad/carga), mayor es el mínimo obligatorio de jugadores escoltas.
- Costo: la caravana SÍ cuesta energía, aunque moverse solo no la cueste, porque compromete el tiempo y la energía de los escoltas. El costo sube con el tamaño del nodo y con la distancia.
- El costo de energía se reparte EQUITATIVAMENTE entre todos los escoltas (ej.: 20 de energía entre 4 jugadores = 5 cada uno).
- Puede ser emboscada por monstruos (PvE) y por otros jugadores (PvP).
- Si es derrotada: el atacante se lleva parte de la carga. Los aldeanos NO mueren; regresan al asentamiento, pero pierden gran parte del material. Al dueño le llega un mensaje: la caravana fue atacada, los aldeanos lograron volver, pero se perdió gran parte de lo recolectado.
8. ENCARGADO Y JUGADORES DISPONIBLES
- El jugador puede ponerse "disponible para el reino" en cierto momento.
- Un encargado (por ejemplo, de caravanas o de agricultura) gasta la energía de los jugadores disponibles dirigiéndola a tareas y destinos específicos.
- Pendiente de definir: si el encargado es un cargo asignado (alcalde, oficial del gremio) y si el jugador puede retirarse mientras está disponible.
9. TUTORIAL INICIAL
Orden exacto de los pasos del tutorial:
1) Moverse de posición
2) Explorar la zona
3) Recolectar
4) Cazar
5) Aportar al campamento
El jugador aprende primero a sostenerse solo y después entra a la capa Imperio.
PENDIENTES QUE SALIERON DE ESTA PARTE
- ¿El minuto por cuadro es fijo o habrá monturas/mejoras que lo aceleren?
- ¿Mientras el jugador se mueve puede hacer otra cosa o queda ocupado?
- Cargo del encargado y si el jugador disponible puede retirarse.
- Recompensa por completar el tutorial.
- Valores concretos de energía por tamaño de nodo y por distancia de caravana.
```

**Las dos preguntas del mismo mensaje** (resumidas):

1. **Armaduras.** Para cada tipo de armadura (placa, malla, cuero y tela): qué estadística principal prevalece, qué clases de Lost Realms la usan, cuál es su rol y qué estadística debe mejorar cada pieza. En la pregunta dijo que "el Herrero hace placa y malla, el Peletero hace cuero y el Sastre hace tela". Eso choca con D-194, confirmada (cuatro armaduras, cuatro oficios: la malla con un oficio propio, el ⛓️ Mallero), así que no se decidió: quedó como pregunta en **E-143**. **Respuesta:** D-206 (provisional; se confirma en E-168). Este juego no tiene fuerza, agilidad ni intelecto, así que el reparto usa sus cuatro estadísticas: vida, ataque, armadura e iniciativa.
2. **Comida.** Los aldeanos PNJ consumen comida (los jugadores no cuentan como población que come), la granja produce comida sola según la etapa, y los aldeanos hacen funcionar las estructuras y forman las caravanas (eso quedó como D-205). Preguntó cuánta comida come cada aldeano por día, cuánto produce la granja por etapa, cuántos aldeanos hay por etapa y qué pasa si hay déficit. **Respuesta:** D-207 (provisional; se confirma en E-169).

## 2-oct-2026 · Estadísticas, armaduras y habilidades

Pedido del dueño por voz (transcripción tal como llegó):

> Okay, ¿Dónde está el resto de estadísticas de World of Warcraft que te permiten eh, sumar beneficios de algún tipo? No lo estoy viendo. O sea, está dando muy pocas estadísticas. Wow, hay como 40 estadísticas diferentes. Están todas las versiones del WoW, cuáles son las que hay, cómo podemos definir para que dos o tres clases compartan algunas cosas. De esta manera lo que pasa es que eh, las clases se equipen con ese equipamiento. Vamos a dejar únicamente tres tipos, placa, cuero y tela. No va a haber malla. Y hay que corregir entonces las clases y lo demás. Vamos a mantener únicamente cuatro habilidades por eh, especialización, no más que eso. Y vamos a reformular todo. Básate en el World of Warcraft en todas sus versiones y cómo podemos ajustarlo. Teniendo en cuenta todas las estadísticas y todas las cosas que se pueden mejorar dentro de eh, las clases.

**Qué se registró:** D-208 (tres armaduras, sin malla), D-209 (cuatro habilidades por especialización) y D-210 (reformular estadísticas y clases según el WoW de todas sus versiones), confirmadas. La propuesta de Claude es D-211 (provisional): [Estadísticas](../03-personaje/estadisticas.md). Las dudas quedaron en E-170 a E-176.

## 2-oct-2026 · Mapa en blanco y clases propias

Pedido del dueño por voz (transcripción tal como llegó):

> Pásame el sistema de preguntas que necesitas para pasar a la otra IA y seguir respondiendo todas las preguntas. Y vas a devolver también el mapa color blanco a medida que vas investigando. Es que vas desbloqueando los colores del mapa, cómo está compuesto. Hasta que no investigas un 50% del mapa, el color no cambia. O sea, de la posición donde estés.
> Así nadie sabe dónde está nada, a no ser que haya ido a investigar o le compre contenido a un investigador.
> O sea, te faltan las habilidades de ataque, defensa, crítico, eh, agilidad y cosas así. O sea, un conjunto de habilidades que eh, el aumento específico de un grupo de estadísticas, aunque todos los jugadores tengan esas estadísticas, el aumento específico de una hace mejor a tu player que el resto. Investiga bien cómo funcionan eh, todas las estadísticas del World of Warcraft. Busca capturas. de las estadísticas y información en foros. Ten en cuenta que la idea es resumir y vamos a crear clases personalizadas. O sea, no va a ser específicamente la del World of Warcraft. La de World of Warcraft era para que tuvieras una idea de cómo funcionaría.
> No era haciendo nada, simplemente mándame el conjunto de preguntas que necesitas antes de continuar. Y ve si sigue dándole el orden de prioridades a las herramientas y todo lo demás.

**Cómo se interpretó:** "no era haciendo nada" se tomó como "no programes nada todavía: mándame las preguntas". Se registraron D-212 (mapa en blanco hasta el 50 %), D-213 (la información del mapa se le compra a un investigador) y D-214 (clases personalizadas con afinidades), confirmadas; las dudas quedaron en E-177 a E-186. El ayudante que elegía 4 habilidades de las clases de hoy se detuvo, porque las clases se van a rehacer. Lo investigado sobre las estadísticas del WoW está en [Estadísticas](../03-personaje/estadisticas.md) §3.1.

## 2-oct-2026 · Estadísticas y clases: contexto decidido en el chat de diseño

El dueño pegó, desde el otro chat, el contexto ya decidido junto con 17 preguntas sobre cómo está el juego hoy:

> - Al subir de nivel, el jugador reparte POCOS puntos, SOLO en estadísticas PRINCIPALES. Las secundarias vienen del equipo, gemas y talentos.
> - El reparto es libre: cada estadística principal da varios beneficios pequeños, así que ninguna es inútil, pero la AFINIDAD de la clase hace que sus estadísticas rindan mucho más. La guía es intuitiva, sin prohibiciones.
> - Todo pasa por rendimiento decreciente con tope, para que nada se rompa (ej.: 40 puntos en crítico NO es 40%).
> - La estadística principal de cada pieza de armadura se ADAPTA a quien la lleva (placa/cuero/tela); la identidad del equipo vive en las secundarias, los bonos de conjunto y las gemas.
> - Se busca que cada jugador se sienta distinto, estilo Dark Souls: estadísticas con función clara y arquetipos dentro de cada rol (tanque de vida vs. tanque de resistencia, DPS de poder vs. DPS de crítico, sanador de ráfaga vs. sanador sostenido).

**Qué se registró:** D-215 a D-219, confirmadas. Cierran E-170, E-183, E-184, E-185 y la parte de conjuntos de E-175. Las 17 preguntas se respondieron con lo que hay hoy en el juego, y lo que falta decidir quedó en E-187 a E-193 (bloque A6). Detalle en [Estadísticas](../03-personaje/estadisticas.md) §3.4.


## 4-oct-2026 · Mapa gris por etapas

Pedido del dueño por voz (transcripción tal como llegó):

> Ok, quiero que regreses a los puntos grises todo el mapa. Y cuando lo investigas al 50%, es que se te va a desbloquear el color, el tipo y la información. O sea, a medida que vas investigando, obviamente vas a ir desbloqueando qué, qué materiales vas encontrando, qué esto, qué lo otro, pero... Eh, debes, en, debes hacerlo de diferentes eh, formas o maneras. ¿Sabes? Para que se vea que vas de, de, eh, desarrollándote poco a poco.

**Cómo se interpretó:** "todo el mapa" responde E-177: todas las zonas en puntos grises salvo el 🔥 Claro. "De diferentes formas o maneras" se tomó como etapas que se ven distintas en el mapa y avisan distinto al explorar: ▫️ sin investigar, ◽ con rastros desde el 1 %, ◻️ reconocida desde el 25 % y, al 50 %, el color de la zona y su tipo de terreno en la leyenda (🎨, y 🆕 la primera vez que ves un terreno); los materiales siguen apareciendo al 1, 20, 40, 60, 80 y 100 %. E-178, E-179 y E-181 se aplicaron con la recomendación.

**Qué se registró:** D-220, confirmada (precisa D-212), en el juego desde la 0.30. Queda por confirmar si tu territorio se ve a color (E-177) y si las etapas te gustan así (E-194, nueva). Detalle en [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.9.
