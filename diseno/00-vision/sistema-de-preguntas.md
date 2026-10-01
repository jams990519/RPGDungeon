# Sistema de preguntas

> **Módulo** [00 · Visión](README.md) · **Depende de:** [Preguntas abiertas](preguntas-abiertas.md), [Entrevista de voz](entrevista-de-voz.md), [Cuestionario de beta](cuestionario-beta.md), [Decisiones](decisiones.md) · **Alimenta a:** todo el diseño y la cola de trabajo · **Estado:** en uso

**Qué es.** El único lugar con **todas** las preguntas que el dueño tiene que responder sobre el juego: las de la entrevista de voz (E-xx), las preguntas abiertas del diseño (P-xx) y las de antes de abrir la beta (C-xxx). Lo pidió el dueño el 1-oct-2026: "el producto es un sistema de preguntas que tienes con respecto a todo".

## Cómo funciona

1. **Un solo texto para copiar.** El bloque de abajo se pega en un chat de voz. El entrevistador va **tanda por tanda**, de lo que frena trabajo a lo que puede esperar, y al final de cada tanda pregunta si sigue o para.
2. **Se puede cortar cuando sea.** El resumen trae solo lo que se alcanzó a ver y el último código ("hasta dónde llegamos"). La vez siguiente se pega el texto actualizado, que ya no trae lo respondido.
3. **Cada respuesta se registra.** Claude la anota como decisión confirmada (D-xx) y marca su P-xx o C-xxx como decidida. Las que digan "recomendación" se toman con lo recomendado.
4. **Las dudas nuevas entran aquí.** Toda duda nueva para el dueño se agrega a este sistema con su código (el siguiente E-xx libre), su P-xx en [Preguntas abiertas](preguntas-abiertas.md) y una recomendación. Nada se pregunta dos veces: lo que ya respondió una decisión se cierra antes de preguntar.
5. **Lo que depende de una respuesta espera.** La cola de trabajo no arranca lo que dependa de una pregunta de la tanda 1 hasta tener la respuesta.

## Estado (1-oct-2026)

| Tanda | De qué trata | Preguntas | Estado |
|---|---|---|---|
| 1 | Lo que frena trabajo: prioridades, asentamiento y castillo, horarios, día y noche, razas y facciones, economía, mazmorras, eventos, enfermedades | 37 | sin responder |
| 2 | PvP, detalles de lo que ya está en el juego, comunidad, plataforma y dinero | 17 | sin responder |
| 3 | Preguntas viejas del diseño que siguen abiertas (P-08 a P-68) | 24 | sin responder |
| 4 | Antes de abrir la beta a más jugadores (primera tanda del cuestionario de beta) | 11 | sin responder |
| 5 | El resto del [Cuestionario de beta](cuestionario-beta.md), limpio de lo que ya respondieron las decisiones | — | en preparación |

**Ya respondidas** (por la entrevista de voz y la ampliación de diseño): D-118 a D-173. **Cerradas al armar este sistema**, porque una decisión posterior ya las respondía: P-02 (D-23), P-09 (sin efecto por D-58), P-11 (D-126; su duración va en E-63), P-14 y P-71 (D-83 y D-94), P-15 (va en E-66), P-45 (D-78 y D-164), P-55 (sin efecto por D-98), P-59 (D-41), P-67 (D-82) y P-69 (D-146). Del cuestionario de beta, C-031 ya estaba resuelta, C-002 se juntó con C-000 y C-103 quedó sin efecto (D-98: el Claro ya no crece).

## El texto para copiar

```text
Eres mi entrevistador para el diseño de "Lost Realms", un juego de rol (RPG) por turnos y en texto que se juega en Telegram (@LostRealmsbot). Yo soy el dueño del juego. Este es el SISTEMA DE PREGUNTAS: todas las dudas que quedan sobre el juego, en tandas, de lo que frena trabajo a lo que puede esperar. Vamos a hablar por voz: tú preguntas y yo respondo.

CÓMO TRABAJAS
1. Haz UNA pregunta a la vez, en español, corta y clara. Lee el código (por ejemplo "E-55" o "C-001"), la frase de contexto y las opciones. Di cuál es la recomendada.
2. Yo puedo responder con una opción, con mis palabras, decir "lo que recomiendes", "siguiente" o "no sé". Si mi respuesta es confusa, repítela en una frase para confirmar y sigue.
3. No me expliques el juego entero: con el contexto de cada pregunta basta. Si pregunto algo que no sabes, dime que lo anotas como duda.
4. Ve tanda por tanda, en orden. Al terminar cada tanda, pregúntame si sigo con la siguiente o paramos.
5. Si digo "pausa", espera. Si digo "termina" o "paramos", ve directo al resumen con lo respondido hasta ahí.
6. No inventes respuestas. Si no respondí, escribe "sin respuesta".

LAS PREGUNTAS

===== TANDA 1 · LO QUE FRENA TRABAJO =====
BLOQUE A · Sin responder y prioridades
E-03 (D-117) Elegiste dejar el nivel 100 en unos 2 años. ¿Entonces lo que hace largo al juego son las dos cosas: subir de nivel y también la historia, el rol, los oficios y el castillo? Sí, las dos (recomendado) / solo la historia y el rol, y que subir sea más rápido.
E-10 Tono del mundo. Opciones: oscuro y serio / épico y heroico / oscuro pero con esperanza y algo de humor (recomendado).
E-52 ¿Qué quieres primero de lo que falta? Ordena: asentamiento por etapas y castillo / razas y facciones nuevas / mazmorras de grupo y jefes de mundo / subasta entre jugadores y desgaste del equipo / enfermedades, médico y alquimista / PvP y bandidos / día, tarde y noche / eventos, temporadas y logros.

BLOQUE B · Asentamiento, castillo y horarios
E-55 (P-78) Mínimo de miembros para pedir castillo. Dijiste de 40 a 50, pero en la beta habrá pocos jugadores. Opciones: 15 durante la beta y 40 desde el lanzamiento (recomendado) / 40 desde ya / otro número.
E-56 (P-79) Para aprobar el castillo, ¿cuántas oleadas seguidas hay que defender y cuántas victorias de cuántos miembros pide la Noche de prueba? Recomendado: 6 oleadas en dos semanas, ganando al menos 4, y una Noche de prueba con 10 victorias de al menos 5 miembros distintos. ¿Está bien o cambias los números?
E-57 (P-80) La casa del inicio: ¿es el primer escalón del asentamiento (la casa crece y se vuelve campamento, aldea, ciudad...) o cada jugador tiene además su propia casa dentro del asentamiento? Opciones: la casa es el primer escalón, compartido por 3 a 5 jugadores (recomendado) / cada uno tiene su casa aparte / las dos cosas.
E-58 (P-81) Etapas del asentamiento: quieres más de 7 (Ashes of Creation tiene 7). Propongo 10: casa, campamento, aldea, pueblo, villa, ciudad, fortaleza, castillo, ciudadela y reino; las primeras rápidas y las últimas lentas. ¿Te sirven 10 y esos nombres, o cuántas y cuáles?
E-59 (P-82) Monarquía y votación: si en el castillo todo se vota, ¿qué decide solo el monarca? Recomendado: el fundador es el monarca y decide el nombre, la bandera, declarar la guerra y aceptar o echar miembros; todo lo demás se vota. ¿Así u otra idea?
E-60 (P-83) Las oleadas contra los campamentos: ¿en días y horas fijas iguales para todos (por ejemplo lunes, miércoles y viernes a las 8 de la noche) o cada campamento con su propio ritmo desde que se fundó? Opciones: días y horas fijas, avisadas (recomendado, como pediste para combates y eventos) / cada uno su ritmo.
E-61 (P-84) Hora de referencia para los eventos fijos (oleadas, asedios, jefes de mundo). Recomiendo la noche de América, de 7 a 11 de la noche en hora de Colombia, Perú o Ecuador (UTC−5). ¿Te sirve u otra?
E-62 (P-85) Guerra de castillos: ¿quién puede atacar a quién? Recomendado: solo los castillos declaran la guerra; pueden atacar desde aldea para arriba, y un asentamiento recién fundado tiene 2 semanas de protección. Otras opciones: cualquiera contra cualquiera / solo castillo contra castillo.

BLOQUE C · Día y noche, razas y facciones
E-63 (P-86) Día, tarde y noche: ¿cuánto dura un día del mundo? Si dura justo un día real, quien juega siempre a la misma hora ve siempre la misma franja. Opciones: 4 días reales (recomendado: cada franja dura unas 32 horas y todos ven las tres) / 1 día real / otro.
E-64 (P-87) ¿Las franjas cambian también el peligro? Por ejemplo, de noche salen enemigos más fuertes con mejor botín. Sí (recomendado) / no, solo cambian los recursos.
E-65 (P-88) Razas: ¿clásicas de la fantasía con nombres e historia propios de este mundo (humanos, elfos, enanos, orcos, medianos, bestiales...) o razas inventadas desde cero? Clásicas con historia propia (recomendado) / inventadas.
E-66 (P-89) ¿Cuántas razas al empezar, y la raza limita qué clases puedes elegir? Recomendado: 6 razas, todas pueden ser cualquier clase y la raza solo da un beneficio chico de oficio y de arma / con límites de clase como en World of Warcraft.
E-67 (P-90) Los héroes que ya existen, ¿eligen raza una vez gratis, como pasó con el origen? Sí (recomendado) / quedan como humanos.
E-68 (P-91) ¿La facción de los ladrones es la casa de los bandidos (los que atacan jugadores y transportes)? Sí (recomendado) / no, son cosas separadas.

BLOQUE D · Economía y oficios
E-69 (P-92) Subasta global con transportistas: ¿dónde recibes lo que compras y cuánto tarda? Recomendado: llega a tu asentamiento o al Claro, tarda según la distancia (de minutos a unas horas) y puedes pagar más para que llegue antes. Otras: llega al instante / otra idea.
E-70 (P-93) Desgaste generoso del equipo. Recomendado: una pieza aguanta unas 3 semanas jugando todos los días antes de pedir reparación; cada reparación le baja un poco el máximo, y tras unas 5 reparaciones se rompe del todo (unos 4 meses de vida). ¿Bien, más o menos?
E-71 (P-94) ¿Las obras maestras firmadas también se gastan? Recomendado: sí, pero aguantan el doble / no se gastan nunca / igual que las normales.
E-72 (P-95) Hoy vender al mercader una obra maestra deja un poco más (un 3,7 %) de lo que valen sus materiales. ¿Lo bajo para que fabricar y vender al mercader no sea negocio? Bajarlo (recomendado: el dinero de verdad debe venir de venderle a otros jugadores) / dejarlo así.
E-74 (P-97) Tope diario de recursos en tu territorio. Recomendado: cada zona da un total por día; pasado ese total, rinde la mitad, y por eso conviene salir a los alrededores. ¿Así?

BLOQUE E · Mazmorras, eventos, enfermedades y fusión
E-83 (P-106) Arena: ¿una arena para pelear contra otros jugadores sin perder nada, desde el principio (también en la beta)? Sí (recomendado: se practica sin riesgo y ayuda a balancear las clases) / no / más adelante.
E-84 (P-107) Eventos y temporadas. Recomendado: un evento corto cada mes (unas 2 semanas, con su historia y su botín) y temporadas de 3 meses con premios cosméticos y una tabla de clasificación; el progreso del héroe nunca se borra. ¿Así u otra idea?
E-85 (P-108) Jefes de mundo. Recomendado: aparecen en lugares del mapa a horas avisadas (la hora de referencia de E-61) para muchos jugadores a la vez, y el botín se reparte según lo que hizo cada uno en su rol (daño, tanque o curación). ¿Así?
E-86 (P-109) Logros y rangos. Recomendado: logros de todo (combate, oficios, exploración, historia, campamento) que dan títulos, marcos y emblemas sin poder de combate, y rangos por temporada. ¿Así?
E-87 (P-110) PvP dentro de las mazmorras: no, las mazmorras son siempre contra monstruos (recomendado) / sí, en algunas mazmorras marcadas / sí, en todas.
E-88 (P-111) Botín no cortado a tu medida: hoy el 70 % de las piezas que caen son de tu tipo. Recomendado: bajarlo al 40 % cuando exista la subasta, para que el resto lo vendas a quien lo necesite / bajarlo ya / otro número.
E-89 (P-112) Fusión de un campamento chico con un castillo. Recomendado: se anuncia con 7 días de aviso; lo que muden los miembros en esos días se conserva, y el castillo recibe la mitad de lo que costaron las obras del campamento; lo que no se mudó se pierde. ¿Así?
E-90 (P-113) Vasallos, como en Ashes of Creation: ¿los asentamientos grandes pueden tener a los chicos como vasallos? Más adelante, junto con la guerra de castillos (recomendado) / no / sí, desde ya.
E-91 (P-114) Enfermedades: ¿desde cuándo aparecen? Recomendado: las primeras, leves, desde el nivel 15 y lejos del Claro; las graves, y las que siguen después de morir, desde el nivel 40. ¿Así?

BLOQUE F · Dudas nuevas
E-92 (P-115) Cuando el campamento defiende bien una oleada, hoy igual pierde 1 punto de defensa (y 2 si la pierde). Con 3 oleadas por semana el daño se junta rápido. Recomendado: defenderla bien no daña nada; solo dañan las que se pierden / dejarlo como está.
E-93 (P-116) Beneficios de oficio del campamento (cocina, pesca, cantería, construcción): hoy cuenta el mejor miembro del grupo en cada oficio. Recomendado: así, el mejor del grupo / se suman los de varios miembros.
E-94 (P-117) Mazmorras de grupo: dijiste que tanque y curador necesitan recompensa propia. Recomendado: todos ganan lo mismo por terminar, y el tanque y el curador se llevan además un cofre extra, porque son los roles que menos se eligen. ¿Así u otra forma?
E-95 (P-118) ¿Cómo se arma un grupo? Recomendado: con los que están en tu misma zona, con un botón para formar grupo y otro para sumarse (como dijiste) / también invitando por nombre a alguien que está lejos.
E-96 (P-119) Los nodos que mejora el carpintero: ¿para quién son? Recomendado: en zonas libres, la mejora sirve a todos; dentro del territorio de un campamento, solo a sus miembros. Duran unos días y hay que mantenerlas. ¿Así?
E-97 (P-120) La información de enfermedades que cazadores e investigadores les pasan a médicos y alquimistas: ¿es un objeto que se puede vender? Recomendado: sí, un informe que se consigue al encontrar la enfermedad y que se vende o se regala / no, se comparte gratis y sin objeto.

===== TANDA 2 · PVP, DETALLES Y COMUNIDAD =====
BLOQUE G · PvP y nodos
E-75 (P-98) ¿Cómo se marcan las zonas de PvP? Recomendado: según la distancia al Claro: cerca, seguras; a media distancia se pierde el 10 % de la mochila; lejos, el 20 %; muy lejos, el 40 %. Los asentamientos siempre seguros. ¿Así u otra forma?
E-76 (P-99) ¿Cuándo entra el PvP? Después de la beta, cuando haya suficientes jugadores (recomendado) / ya en la beta.
E-78 (P-101) Los nodos especiales que descubren los expertos: ¿de quién hay que defenderlos? De monstruos que aparecen (recomendado al principio) / de otros jugadores, cuando haya PvP / de los dos.

BLOQUE H · Detalles de lo que ya está en el juego
E-79 (P-102) Explorador: los que ya exploraban antes de que existiera el oficio, ¿reciben experiencia de Explorador por lo que exploraron? Sí, una parte (recomendado) / no, todos empiezan desde cero.
E-80 (P-103) Si fundas o agrandas tu asentamiento donde hay un campamento enemigo, ¿se prohíbe hasta destruirlo? Sí (recomendado) / no, el campamento enemigo desaparece.
E-81 (P-104) Los jefes de los campamentos enemigos lejanos, ¿piden grupo? Sí, desde cierta distancia (recomendado) / no, siempre se pueden hacer solos.
E-82 (P-105) Cambiar de especialización de oficio: dijiste que se puede pagando y empezando de cero en la nueva. Lo dejé así: elegir la primera y la segunda es gratis; cambiar cuesta 1 de plata más 20 de bronce por rango (unas 6 de plata al rango 25 y 21 al rango 100), y lo aprendido en la vieja queda guardado por si vuelves. ¿Está bien o lo cambias?

BLOQUE I · Comunidad, plataforma y dinero
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

===== TANDA 3 · PREGUNTAS VIEJAS DEL DISEÑO QUE SIGUEN ABIERTAS =====
BLOQUE J · Combate en grupo y PvP
E-98 (P-08) ¿Un solo servidor, un solo mundo para todos los jugadores, o varios? Recomendado: uno solo mientras quepa, como pide la regla de un solo mundo / varios servidores.
E-99 (P-17) Peleas en grupo: ¿tiempo límite por ronda? Recomendado: 45 segundos en mazmorras de grupo y de 60 a 90 en bandas grandes; jugando solo, sin tiempo límite. ¿Así?
E-100 (P-18) Si en una pelea de grupo no respondes a tiempo, ¿tu héroe actúa solo, como en las peleas automáticas? Recomendado: sí, salvo contra Guardianes y en la arena clasificada / no, pierde el turno.
E-101 (P-19) En PvP, ¿se puede apuntar a partes del cuerpo (cabeza, piernas) para herir? Recomendado: sí, con menos probabilidad de acertar / no.
E-102 (P-30) En la arena clasificada, ¿todos pelean con equipo igualado para que gane el más hábil? Recomendado: sí en la clasificada; en la arena libre, cada uno con su equipo / no, cada uno con lo suyo siempre.
E-103 (P-29) ¿Invasiones al estilo Dark Souls, donde otro jugador entra a tu zona a cazarte? Recomendado: solo en zonas y modos marcados, con aviso / no.

BLOQUE K · Economía, construcción y salud
E-104 (P-33) ¿Un mercado negro donde se vende lo robado y piezas raras? Recomendado: sí, ligado a la facción de los ladrones, más adelante / no.
E-105 (P-53) Puestos y locales del asentamiento: ¿tasa autodeclarada? Declaras cuánto vale tu puesto, pagas impuesto por ese valor y otro puede comprártelo a ese precio. Recomendado: sí para puestos y locales; las casas, con tasa fija / no.
E-106 (P-51) Construir: ¿por planos con opciones o pieza por pieza libre? Recomendado: planos con opciones para la estructura y decoración libre / todo libre.
E-107 (P-24) Estrés del héroe por peleas duras o muertes cercanas, con malestares que se curan descansando. Recomendado: sí, una capa ligera, más adelante / no.
E-108 (P-40) Enfermedades de oficio (por ejemplo, el minero que tose de tanto picar). Recomendado: sí, leves, cuando entren las enfermedades / no.
E-109 (P-56) Suciedad e higiene (baños, termas). Recomendado: sí, ligera / no.

BLOQUE L · Contenido para más adelante
E-110 (P-25) Vampirismo y licantropía jugables. Recomendado: sí, en una expansión / no.
E-111 (P-57) Panteón de dioses con sacerdotes que son jugadores. Recomendado: sí, en la primera expansión / no.
E-112 (P-49) Casos de investigación semanales para todo el servidor, con clasificación. Recomendado: sí / no.
E-113 (P-41) ¿Qué minijuegos van primero? Recomendado: dados de taberna, preguntas sobre la historia del mundo y rezar en el santuario. ¿Esos u otros?
E-114 (P-68) La técnica de arma (idea de Albion Online): ¿ocupa una de las 3 casillas de habilidad en combate? Recomendado: que pueda ocupar una, a elección del jugador / se quita.

BLOQUE M · Plataforma, servidores y tiendas
E-115 (P-44) En Telegram, ¿solo chat o también una Mini App (una ventanita dentro de Telegram) para el mapa, los talentos y la subasta? Recomendado: solo chat primero y la Mini App después / la Mini App ya.
E-116 (P-46) Hoy el juego guarda todo en un archivo de base de datos dentro de Railway. Recomendado: pasar a una base de datos PostgreSQL antes de abrir a 500 jugadores, sin perder nada / más adelante, cuando haga falta.
E-117 (P-47) ¿Cuánto quieres gastar como máximo al mes en servidores? Dime un tope. Recomendado: fijarlo ahora y que yo te avise al llegar al 80 %.
E-118 (P-48) ¿Una API pública de solo lectura para que la comunidad haga herramientas (mapas, calculadoras)? Recomendado: sí, durante la beta / no.
E-119 (P-60) La página web: ¿qué dominio y dónde se aloja? Recomendado: un dominio propio con el nombre del juego, decidido antes de hacer la web. ¿Tienes uno pensado?
E-120 (P-62) ¿La app va a las tiendas de Apple y Google? Recomendado: sí, más adelante; ahí los pagos pasan por cada tienda / no, solo web instalable.
E-121 (P-63) Edad mínima en las tiendas: con apuestas, aunque sean con oro del juego, suele pedirse 17 o 18 años. Recomendado: mantener las apuestas solo con oro del juego y aceptar 17+ / quitar las apuestas para bajar la edad.

===== TANDA 4 · ANTES DE ABRIR LA BETA A MÁS JUGADORES =====
BLOQUE N · Apertura y pruebas
C-001 ¿Los jugadores de la beta entran al mismo @LostRealmsbot de hoy, y ese mundo es el definitivo, sin borrado? Recomendado: sí, un solo mundo sin borrado, anunciado como acceso anticipado / un mundo de beta que se borre.
C-000 ¿Abrimos a 500 jugadores con lo que hay hoy o esperamos un parche de beta con lo mínimo para tanta gente (herramientas de moderación, copias de seguridad probadas, modo mantenimiento y tope de jugadores con cola)? Recomendado: esperar ese parche, de 1 a 2 semanas / abrir ya / abrir a una parte ya.
C-003 ¿La beta se abre solo cuando se cumpla esa lista de condiciones, aunque mueva la fecha? Recomendado: sí / no, con fecha fija.
C-004 Antes de abrir a 500, ¿una prueba cerrada de 1 a 2 semanas con 30 a 50 jugadores de confianza? Recomendado: sí / no.
C-033 Bot de pruebas: el cuestionario viejo proponía usar @thetowerwarbot, que quedó libre. Como TowerWars no se toca, recomiendo crear un bot de pruebas nuevo para Lost Realms, con su propia base de datos. ¿Creamos uno nuevo (recomendado) o usamos ese?
C-034 ¿Me das permiso para crear en Railway un servicio aparte para el bot de pruebas, con su propio volumen? Hoy solo toco el servicio RPGDungeon. Recomendado: sí, así se prueba sin tocar el juego en vivo / no.
C-032 Desde la beta, ¿sigue el piloto automático que publica solo cada parche probado, o apruebas tú los grandes? Recomendado: sigue solo para arreglos y ajustes; los parches grandes los apruebas tú con un mensaje / todo automático / todo lo apruebas tú.

BLOQUE O · Moderación y reglas
C-050 Herramientas mínimas de moderación para el primer día: reportar, ver transferencias, congelar el comercio, suspender, banear y devolver objetos. Recomendado: sí, esas / agrega o quita alguna.
C-011 Hoy cualquiera entra al bot con /start. ¿Lo dejamos abierto en la beta? Recomendado: abierto, con tope de jugadores y cola / solo con invitación.
C-068 ¿Cada jugador acepta con un botón, al entrar, unas reglas cortas? Recomendado: sí / no.
C-067 ¿@LostRealmsbot tiene su propia política de privacidad o usa la de Telegram? Recomendado: una propia, corta y en español / la de Telegram.

FORMATO DEL RESUMEN FINAL (escríbelo así, sin nada más antes ni después):
RESPUESTAS LOST REALMS · SISTEMA DE PREGUNTAS
E-03: [opción elegida o respuesta corta] | [detalle o condición, si dijo algo más]
E-10: ...
(una línea por cada pregunta que alcanzamos a ver, en este orden: E-03, E-10, E-52, E-55, E-56, E-57, E-58, E-59, E-60, E-61, E-62, E-63, E-64, E-65, E-66, E-67, E-68, E-69, E-70, E-71, E-72, E-74, E-83, E-84, E-85, E-86, E-87, E-88, E-89, E-90, E-91, E-92, E-93, E-94, E-95, E-96, E-97, E-75, E-76, E-78, E-79, E-80, E-81, E-82, E-44, E-45, E-46, E-47, E-48, E-49, E-50, E-51, E-53, E-54, E-98, E-99, E-100, E-101, E-102, E-103, E-104, E-105, E-106, E-107, E-108, E-109, E-110, E-111, E-112, E-113, E-114, E-115, E-116, E-117, E-118, E-119, E-120, E-121, C-001, C-000, C-003, C-004, C-033, C-034, C-032, C-050, C-011, C-068, C-067; "sin respuesta" si se saltó; "recomendación" si dijo "lo que recomiendes"; las que no alcanzamos a ver, no las pongas)
HASTA DÓNDE LLEGAMOS: [el último código que vimos]
DUDAS: [lo que preguntó y no supiste responder]
IDEAS SUELTAS: [cualquier idea que dijo fuera de las preguntas]
```
