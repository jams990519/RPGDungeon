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
