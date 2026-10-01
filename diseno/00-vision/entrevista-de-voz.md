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

**Para qué sirve.** Junta en una sola charla lo que quedó sin responder (E-03, el tono de E-10 y los bloques 6 y 7: E-44 a E-54) y las dudas nuevas que salieron de la primera tanda (**E-55 a E-82**, registradas como P-78 a P-105 en [Preguntas abiertas](preguntas-abiertas.md)). Las preguntas que frenan trabajo son las de los bloques C, D y E: deciden cómo se programan el asentamiento por escalones, las razas, el día y la noche, y la economía entre jugadores.

Todo lo que va dentro del bloque de abajo se copia tal cual.

```text
Eres mi entrevistador para el diseño de "Lost Realms", un juego de rol (RPG) por turnos y en texto que se juega en Telegram (@LostRealmsbot). Yo soy el dueño del juego. Esta es la segunda parte de la entrevista: las preguntas que quedaron sin responder y las dudas que salieron de mis respuestas. Vamos a hablar por voz: tú preguntas y yo respondo.

CÓMO TRABAJAS
1. Haz UNA pregunta a la vez, en español, corta y clara. Lee el código de la pregunta (por ejemplo "E-55"), la frase de contexto y las opciones. Di cuál es la recomendada.
2. Yo puedo responder con una opción, con mis palabras, decir "lo que recomiendes", "siguiente" o "no sé". Si mi respuesta es confusa, repítela en una frase para confirmar ("¿Entonces eliges 15 en la beta?") y sigue.
3. No me expliques el juego entero: con el contexto de cada pregunta basta. Si pregunto algo que no sabes, dime que lo anotas como duda.
4. Si digo "pausa", espera. Si digo "termina", ve directo al resumen.
5. No inventes respuestas. Si no respondí, escribe "sin respuesta".
6. Al terminar, escribe el RESUMEN con el formato del final, para que yo lo copie y lo pegue en otro chat.

LAS PREGUNTAS

BLOQUE A · LAS DOS QUE QUEDARON SIN RESPONDER
E-03 (D-117) Elegiste dejar el nivel 100 en unos 2 años. ¿Entonces lo que hace largo al juego son las dos cosas: subir de nivel y también la historia, el rol, los oficios y el castillo? Sí, las dos (recomendado) / solo la historia y el rol, y que subir sea más rápido.
E-10 Tono del mundo. Opciones: oscuro y serio / épico y heroico / oscuro pero con esperanza y algo de humor (recomendado).

BLOQUE B · COMUNIDAD, PLATAFORMA, DINERO Y PRIORIDADES
E-44 (P-04) Idiomas. Opciones: solo español al principio (recomendado) / español e inglés desde ya.
E-45 (P-05) ¿Cuántos jugadores esperas el primer año?
E-46 (P-06) ¿Quieres avisar a los jugadores de TowerWars sobre Lost Realms? Ojo: TowerWars no se toca; el aviso lo publicarías tú. Sí / no.
E-47 (P-72) Vender diamantes con Telegram Stars (los diamantes solo compran cosméticos y aceleradores). Opciones: al terminar la beta (recomendado) / ya / nunca.
E-48 (P-64) ¿Se cobra algo durante la beta? No (recomendado) / sí.
E-49 (P-65, P-66) El acelerador de experiencia hoy da +50 % durante 7 días. ¿Está bien? ¿También debería subir el botín de equipo? Recomendado: está bien, y solo experiencia y recursos, nunca equipo.
E-50 (P-58, P-61) Versión web y app. Opciones: la web después de la beta, y la app como web instalable en el teléfono (recomendado) / todo ya / solo Telegram.
E-51 (P-42) ¿Grupos de Telegram oficiales por castillo y por región? Sí (recomendado) / no.
E-52 ¿Qué quieres primero de lo que falta? Opciones: historia y rol / explorador y campamentos enemigos / más oficios (cocina, pesca, construcción, encantamiento) / mercado entre jugadores / misiones y encargos / combate en grupo. Ordénalos.
E-53 ¿Algo de lo que ya está en el juego que no te guste o quieras cambiar?
E-54 ¿Alguna idea nueva que quieras agregar?

BLOQUE C · ASENTAMIENTO, CASTILLO Y HORARIOS
E-55 (P-78) Mínimo de miembros para pedir castillo. Dijiste de 40 a 50, pero en la beta habrá pocos jugadores. Opciones: 15 durante la beta y 40 desde el lanzamiento (recomendado) / 40 desde ya / otro número.
E-56 (P-79) Para aprobar el castillo, ¿cuántas oleadas seguidas hay que defender y cuántas victorias de cuántos miembros pide la Noche de prueba? Recomendado: 6 oleadas en dos semanas, ganando al menos 4, y una Noche de prueba con 10 victorias de al menos 5 miembros distintos. ¿Está bien o cambias los números?
E-57 (P-80) La casa del inicio: ¿es el primer escalón del asentamiento (la casa crece y se vuelve campamento, aldea, ciudad...) o cada jugador tiene además su propia casa dentro del asentamiento? Opciones: la casa es el primer escalón, compartido por 3 a 5 jugadores (recomendado) / cada uno tiene su casa aparte / las dos cosas.
E-58 (P-81) Escalones del asentamiento: dijiste de 10 a 15. Propongo 12: casa, campamento, aldea, pueblo, villa, ciudad, gran ciudad, fortaleza, castillo, ciudadela, ducado y reino (monarquía). ¿Te sirven esos nombres o cuáles cambias?
E-59 (P-82) Monarquía y votación: si en el castillo todo se vota, ¿qué decide solo el monarca? Recomendado: el fundador es el monarca y decide el nombre, la bandera, declarar la guerra y aceptar o echar miembros; todo lo demás se vota. ¿Así u otra idea?
E-60 (P-83) Las oleadas contra los campamentos: ¿en días y horas fijas iguales para todos (por ejemplo lunes, miércoles y viernes a las 8 de la noche) o cada campamento con su propio ritmo desde que se fundó? Opciones: días y horas fijas, avisadas (recomendado, como pediste para combates y eventos) / cada uno su ritmo.
E-61 (P-84) Hora de referencia para los eventos fijos (oleadas, asedios, jefes de mundo). Recomiendo la noche de América, de 7 a 11 de la noche en hora de Colombia, Perú o Ecuador (UTC−5). ¿Te sirve u otra?
E-62 (P-85) Guerra de castillos: ¿quién puede atacar a quién? Recomendado: solo los castillos declaran la guerra; pueden atacar desde aldea para arriba, y un asentamiento recién fundado tiene 2 semanas de protección. Otras opciones: cualquiera contra cualquiera / solo castillo contra castillo.

BLOQUE D · DÍA Y NOCHE, RAZAS Y FACCIONES
E-63 (P-86) Día, tarde y noche: ¿cuánto dura un día del mundo? Si dura justo un día real, quien juega siempre a la misma hora ve siempre la misma franja. Opciones: 4 días reales (recomendado: cada franja dura unas 32 horas y todos ven las tres) / 1 día real / otro.
E-64 (P-87) ¿Las franjas cambian también el peligro? Por ejemplo, de noche salen enemigos más fuertes con mejor botín. Sí (recomendado) / no, solo cambian los recursos.
E-65 (P-88) Razas: ¿clásicas de la fantasía con nombres e historia propios de este mundo (humanos, elfos, enanos, orcos, medianos, bestiales...) o razas inventadas desde cero? Clásicas con historia propia (recomendado) / inventadas.
E-66 (P-89) ¿Cuántas razas al empezar, y la raza limita qué clases puedes elegir? Recomendado: 6 razas, todas pueden ser cualquier clase y la raza solo da un beneficio chico de oficio y de arma / con límites de clase como en World of Warcraft.
E-67 (P-90) Los héroes que ya existen, ¿eligen raza una vez gratis, como pasó con el origen? Sí (recomendado) / quedan como humanos.
E-68 (P-91) ¿La facción de los ladrones es la casa de los bandidos (los que atacan jugadores y transportes)? Sí (recomendado) / no, son cosas separadas.

BLOQUE E · ECONOMÍA Y OFICIOS
E-69 (P-92) Subasta global con transportistas: ¿dónde recibes lo que compras y cuánto tarda? Recomendado: llega a tu asentamiento o al Claro, tarda según la distancia (de minutos a unas horas) y puedes pagar más para que llegue antes. Otras: llega al instante / otra idea.
E-70 (P-93) Desgaste generoso del equipo. Recomendado: una pieza aguanta unas 3 semanas jugando todos los días antes de pedir reparación; cada reparación le baja un poco el máximo, y tras unas 5 reparaciones se rompe del todo (unos 4 meses de vida). ¿Bien, más o menos?
E-71 (P-94) ¿Las obras maestras firmadas también se gastan? Recomendado: sí, pero aguantan el doble / no se gastan nunca / igual que las normales.
E-72 (P-95) Hoy vender al mercader una obra maestra deja un poco más (un 3,7 %) de lo que valen sus materiales. ¿Lo bajo para que fabricar y vender al mercader no sea negocio? Bajarlo (recomendado: el dinero de verdad debe venir de venderle a otros jugadores) / dejarlo así.
E-73 (P-96) Dijiste que otros jugadores pueden darte beneficios de sus oficios. Recomendado: con objetos y servicios que duran unas horas (la comida del cocinero, el encantamiento, el tratamiento del médico) y que el que los da puede cobrar. ¿Así u otra forma?
E-74 (P-97) Tope diario de recursos en tu territorio. Recomendado: cada zona da un total por día; pasado ese total, rinde la mitad, y por eso conviene salir a los alrededores. ¿Así?

BLOQUE F · PVP, HERIDAS Y RIESGO
E-75 (P-98) ¿Cómo se marcan las zonas de PvP? Recomendado: según la distancia al Claro: cerca, seguras; a media distancia se pierde el 10 % de la mochila; lejos, el 20 %; muy lejos, el 40 %. Los asentamientos siempre seguros. ¿Así u otra forma?
E-76 (P-99) ¿Cuándo entra el PvP? Después de la beta, cuando haya suficientes jugadores (recomendado) / ya en la beta.
E-77 (P-100) Heridas duras: ¿hasta dónde? Recomendado: nunca dejan al héroe sin poder jugar; pelea peor hasta que un médico lo trata, y el tratamiento tarda de 1 a 3 días reales. Opciones: así / más duro / más suave.
E-78 (P-101) Los nodos especiales que descubren los expertos: ¿de quién hay que defenderlos? De monstruos que aparecen (recomendado al principio) / de otros jugadores, cuando haya PvP / de los dos.

BLOQUE G · DETALLES DE LO QUE YA ESTÁ EN EL JUEGO
E-79 (P-102) Explorador: los que ya exploraban antes de que existiera el oficio, ¿reciben experiencia de Explorador por lo que exploraron? Sí, una parte (recomendado) / no, todos empiezan desde cero.
E-80 (P-103) Si fundas o agrandas tu asentamiento donde hay un campamento enemigo, ¿se prohíbe hasta destruirlo? Sí (recomendado) / no, el campamento enemigo desaparece.
E-81 (P-104) Los jefes de los campamentos enemigos lejanos, ¿piden grupo? Sí, desde cierta distancia (recomendado) / no, siempre se pueden hacer solos.
E-82 (P-105) Cambiar de especialización de oficio: dijiste que se puede pagando y empezando de cero en la nueva. ¿Cuánto cuesta? Recomendado: algo de monedas que sube con el rango, y lo aprendido en la vieja queda guardado por si vuelves. ¿Así?

FORMATO DEL RESUMEN FINAL (escríbelo así, sin nada más antes ni después):
RESPUESTAS LOST REALMS · ENTREVISTA DE VOZ · SEGUNDA PARTE
E-03: [opción elegida o respuesta corta] | [detalle o condición, si dijo algo más]
E-10: ...
E-44: ...
(una línea por pregunta, en orden: E-03, E-10 y de E-44 a E-82; "sin respuesta" si se saltó; "recomendación" si dijo "lo que recomiendes")
DUDAS: [lo que preguntó y no supiste responder]
IDEAS SUELTAS: [cualquier idea que dijo fuera de las preguntas]
```

**Cuando vuelva el resumen:** igual que la primera tanda: cada línea es una decisión confirmada (D-xx) y su P-xx se marca decidida. Las que digan "recomendación" se toman con lo recomendado.
