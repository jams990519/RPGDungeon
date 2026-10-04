# Sistema de preguntas

> **Módulo** [00 · Visión](README.md) · **Depende de:** [Preguntas abiertas](preguntas-abiertas.md), [Entrevista de voz](entrevista-de-voz.md), [Cuestionario de beta](cuestionario-beta.md), [Decisiones](decisiones.md) · **Alimenta a:** todo el diseño y la cola de trabajo · **Estado:** en uso

**Qué es.** El único lugar con **todas** las preguntas que el dueño tiene que responder sobre el juego: las de la entrevista de voz (E-xx), las preguntas abiertas del diseño (P-xx) y las de antes de abrir la beta (C-xxx). Lo pidió el dueño el 1-oct-2026: "el producto es un sistema de preguntas que tienes con respecto a todo".

## Cómo funciona

1. **Un solo texto para copiar.** El bloque de abajo se pega en un chat de voz. El entrevistador va **tanda por tanda**, de lo que frena trabajo a lo que puede esperar, y al final de cada tanda pregunta si sigue o para.
2. **Se puede cortar cuando sea.** El resumen trae solo lo que se alcanzó a ver y el último código ("hasta dónde llegamos"). La vez siguiente se pega el texto actualizado, que ya no trae lo respondido.
3. **Cada respuesta se registra.** Claude la anota como decisión confirmada (D-xx) y marca su P-xx o C-xxx como decidida. Las que digan "recomendación" se toman con lo recomendado.
4. **Las dudas nuevas entran aquí.** Toda duda nueva para el dueño se agrega a este sistema con su código (el siguiente E-xx libre), su P-xx en [Preguntas abiertas](preguntas-abiertas.md) y una recomendación. Nada se pregunta dos veces: lo que ya respondió una decisión se cierra antes de preguntar.
5. **Lo que depende de una respuesta espera.** La cola de trabajo no arranca lo que dependa de una pregunta de la tanda 1 hasta tener la respuesta.

## Estado (4-oct-2026)

| Tanda | De qué trata | Preguntas | Estado |
|---|---|---|---|
| 1 | Lo que frena trabajo: prioridades; estadísticas, armaduras, habilidades y clases propias; mapa gris; oficios y granja; viaje, caravanas, tutorial y comida de los aldeanos, asentamiento y castillo, horarios, día y noche, razas y facciones, economía, mazmorras, eventos, enfermedades | 85 | sin responder |
| 2 | PvP, detalles de lo que ya está en el juego (también el mapa y los nodos de las ideas sueltas del 1-oct), el camino guiado y los menús del 2-oct, comunidad, plataforma y dinero | 30 | sin responder |
| 3 | Preguntas viejas del diseño que siguen abiertas (P-08 a P-68) | 24 | sin responder |
| 4 | Antes de abrir la beta a más jugadores (primera tanda del cuestionario de beta) | 11 | sin responder |
| 5 | El resto del [Cuestionario de beta](cuestionario-beta.md), lo que pesa antes de abrir: responsable legal, edad y privacidad, copias y permisos del bot, trampas, moderación y plan de apertura | 43 | sin responder |
| 6 | El resto del cuestionario de beta, lo que puede esperar a la beta: juego, tu comunidad, lanzamiento, operación, salud y nombres | 45 | sin responder |

**Ya respondidas** (por la entrevista de voz, la ampliación de diseño, las ideas sueltas del mapa y los chats del 2-oct): D-118 a D-173, D-178 a D-181, D-185, D-186, D-189 a D-191, D-194 a D-205, D-208 a D-210 y D-212 a D-220. **Cerradas el 2-oct** por las decisiones de diseño (continuación): E-136 (D-198: el Joyero refina las gemas), E-149 (D-199: ranuras en armaduras y armas), E-96 (D-201: nodos internos y externos), E-143 (D-208: ya no hay malla ni Mallero), E-168 (la reemplazan E-170 a E-176) y E-153 (D-205: la granja produce sola); E-154 pasó a E-169 (D-207). **Cerradas al armar este sistema**, porque una decisión posterior ya las respondía: P-02 (D-23), P-09 (sin efecto por D-58), P-11 (D-126; su duración va en E-63), P-14 y P-71 (D-83 y D-94), P-15 (va en E-66), P-45 (D-78 y D-164), P-55 (sin efecto por D-98), P-59 (D-41), P-67 (D-82) y P-69 (D-146). Del cuestionario de beta, C-031 ya estaba resuelta, C-002 se juntó con C-000 y C-103 quedó sin efecto (D-98: el Claro ya no crece).

**Del resto del cuestionario de beta** (146 preguntas escritas con el juego en la 0.6): **15** ya las respondía una decisión (por ejemplo C-122 por D-138 y C-150 por D-135), **19** quedaron sin efecto (el Claro ya no crece, Raigambre se pelea en solitario, los oficios ya están en el juego), **24** estaban repetidas con otras del sistema (por ejemplo C-019 es E-44 y C-134 es E-76) y **88** siguen abiertas en las tandas 5 y 6, reescritas con lo que cambió. Cada una quedó marcada debajo de su título en el [Cuestionario de beta](cuestionario-beta.md).

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

BLOQUE A4 · Estadísticas, armaduras y habilidades (2-oct, documento diseno/03-personaje/estadisticas.md)
E-171 (P-170) Sin malla (D-208), ¿a qué tipo pasan sus clases? (Vale si se mantienen las clases de hoy; con clases propias, cada una ya trae su armadura, E-182.) Recomendado: 🏹 Cazador a cuero (como en el WoW clásico antes del nivel 40), 🌊 Chamán a placa (híbrido pesado de Intelecto, como el Paladín) y 🐲 Evocador a tela; quedan 4 clases en placa, 6 en cuero y 5 en tela / el Chamán a cuero (quedan 3 en placa y 7 en cuero) / otro reparto.
E-172 (P-171) Las 4 habilidades por especialización (D-209): recomendado: ⚔️ Atacar cuenta como una de las 4, o sea Atacar y 3 habilidades, todas en la barra y sin elegir (como ya decía D-46) / 4 habilidades además de Atacar (la barra pasa de 6 botones o hay que elegir 3 de 4).
E-173 (P-172) ¿Cuántas estadísticas? Recomendado: una capa simple de 9 en cada pieza (Fuerza, Agilidad, Intelecto, Vitalidad, Armadura, Crítico, Celeridad, Maestría y Versatilidad) y una capa profunda en piezas raras, gemas y comida (Robo de vida, Evasión, Indestructible, 6 resistencias y, con el PvP, Resiliencia); sin golpe, pericia, defensa ni penetración, que el WoW quitó porque solo obligaban a llegar a un tope / todas las del WoW / menos.
E-174 (P-173) Mejorar las habilidades sin sumar botones: recomendado: filas de talentos como en el WoW de Pandaria: cada 15 niveles (15, 30, 45, 60, 75 y 90) eliges 1 de 3 mejoras que cambian una de tus 4 habilidades o suman un pasivo, y se cambian fuera de combate; la mejora pasiva de hoy por punto se queda / solo la mejora pasiva de hoy / árboles de talentos como el WoW actual.
E-175 (P-174) Otras mejoras de clase del WoW (los bonos de conjunto ya los decidiste, D-218): recomendado: adornos de artesano (efectos especiales en piezas fabricadas, máximo 2) y, más adelante, glifos y reforja con el Encantamiento; sin arma artefacto, azerita, pactos ni runas / otras.
E-176 (P-175) Los jugadores de hoy (D-64, nada se pierde): recomendado: cada pieza de malla se vuelve la misma pieza del tipo nuevo de tu clase (cuero, placa o tela; de otra clase, cuero), la especialización de malla de la Peletería se cambia gratis una vez, las piezas de hoy reciben las estadísticas nuevas sin perder poder y las habilidades que salen se quitan de la barra solas / otra forma.

BLOQUE A5 · Clases propias, afinidades y mapa gris (2-oct y 4-oct, documentos diseno/03-personaje/estadisticas.md y diseno/02-mundo/mapa-infinito-y-viaje.md)
E-182 (P-181) Clases personalizadas (D-214): recomendado: Claude propone un juego de clases propias (unas 8 a 10, con 3 especializaciones cada una), partiendo de las 15 de hoy y juntando las que se parecen, cada una con nombre propio, armadura (placa, cuero o tela), afinidades y sus 4 habilidades; tú eliges y cambias antes de programar / mantener las 15 de hoy con nombres propios / tú dices cuáles.
E-186 (P-185) Los jugadores de hoy cuando lleguen las clases nuevas: recomendado: cambian de clase gratis una vez, conservando nivel, equipo y oficios (después la clase sigue siendo para siempre, D-74) / se les pone la clase nueva más parecida / se quedan con su clase vieja.
E-177 (P-176) Mapa gris (D-220, ya en el juego desde la 0.30): todo el mapa está en puntos grises hasta investigar cada zona al 50 %, salvo el Claro. ¿Tu territorio (las zonas de tu campamento) también se ve a color sin investigarlo? Sí (recomendado) / no, también gris hasta el 50 %.
E-178 (P-177) Los íconos en zonas grises (🕳️ cuevas, ✨ nodos, 👹 campamentos enemigos, jugadores). Así quedó en la 0.30, confirma: siguen sus reglas de siempre (la cueva se marca si estás cerca, el nodo al llegar, el campamento enemigo al verlo), aunque la zona siga gris (recomendado) / también se ocultan hasta el 50 %.
E-179 (P-178) Lo que ya veían los jugadores. Así quedó en la 0.30, confirma: las zonas que exploraron al 50 % o más quedan a color y las demás volvieron a gris; nadie perdió su porcentaje de exploración, solo el color (recomendado) / todo lo que ya veían vuelve a color.
E-180 (P-179) Comprarle el mapa a un investigador (D-213): recomendado: el 🧭 Explorador hace un 🗺️ pergamino de mapa con las zonas que exploró al 50 % o más de una región de 6 × 6, lo vende al precio que quiera, y quien lo usa ve esos colores para siempre / se comparte gratis con tu campamento / otra idea.
E-181 (P-180) "De la posición donde estés". Así quedó en la 0.30, confirma: también cuenta lo que exploras alrededor sin moverte (D-107): si estudias una zona vecina al 50 %, se pinta (recomendado) / solo la zona donde estás parado.
E-194 (P-193) Cómo se descubre una zona "poco a poco" (D-220). Así quedó en la 0.30, confirma: ▫️ sin investigar, ◽ con rastros desde el 1 % (ya encontraste algo), ◻️ reconocida desde el 25 % y, al 50 %, su color y su tipo de terreno; cada paso avisa distinto (◻️ al reconocerla, 🎨 al ver su color, 🆕 la primera vez que ves un terreno, ✅ al 100 %) y los recursos se siguen descubriendo al 1, 20, 40, 60, 80 y 100 %. Así (recomendado) / más pasos (por ejemplo, el nombre del terreno ya al 25 %) / otra forma.

BLOQUE A6 · Estadísticas: puntos, afinidad, tope, armas y arquetipos (2-oct, lo que decidiste: D-215 a D-219; documento diseno/03-personaje/estadisticas.md)
E-187 (P-186) Puntos por nivel (D-215: pocos y solo en principales): recomendado: 1 punto por nivel (99 al llegar al 100), más una base de clase al crear el héroe (por ejemplo 10 puntos ya puestos en sus afinidades) / 2 por nivel / 3 cada 5 niveles.
E-188 (P-187) ¿Qué estadísticas principales hay y qué da cada una (D-216: varios beneficios pequeños)? Recomendado: 5: 💪 Fuerza (daño de golpes, parada y bloqueo), 🏹 Agilidad (daño de golpes, esquiva, algo de crítico e iniciativa), 🔮 Intelecto (daño de hechizos, poder de curas y maná), ❤️ Vitalidad (vida máxima, vida que vuelve sola y resistencia a enfermedades) y 🕊️ Voluntad (recurso que vuelve cada ronda, curas por ronda y resistencia a estados como miedo, aturdimiento o veneno) / solo las 4 primeras, sin Voluntad / otra lista.
E-189 (P-188) ¿Cuánto más rinde la afinidad (D-216: "mucho más")? Recomendado: ×1,5: lo que pones en tus estadísticas afines (2 de la clase y 1 de la especialización) rinde 50 % más; las demás rinden normal / +25 % / ×2.
E-190 (P-189) La fórmula del rendimiento decreciente (D-217): recomendado: las secundarias rinden completas hasta 30 %, a la mitad entre 30 y 50 %, y no pasan de 50 %; los puntos de principales rinden completos hasta el doble de tu nivel y a la mitad después; y cuántos puntos hacen falta para 1 % crece con el nivel, como en el WoW / otra fórmula.
E-191 (P-190) ¿Los puntos repartidos se reajustan? Recomendado: sí, pagando como hoy los talentos (10 💰 por nivel), y gratis una vez cuando llegue el sistema nuevo / gratis una vez por semana / son permanentes.
E-192 (P-191) Armas al estilo Dark Souls: recomendado: cada tipo de arma escala con una principal o dos (espada, hacha y maza con Fuerza; daga y arco con Agilidad; bastón y varita con Intelecto; espada ligera con Fuerza y Agilidad); cualquier clase puede usar cualquier arma, pero las de su clase rinden completas (hoy las otras rinden la mitad, D-83); los tipos nuevos llegan con las clases propias / sin escalado, el arma solo da ataque como hoy.
E-193 (P-192) Arquetipos de cada rol (D-219): recomendado: tanque de vida = Vitalidad, Robo de vida y Versatilidad (aguanta y se cura); tanque de resistencia = Armadura, Maestría de bloqueo o esquiva y resistencias (recibe menos); DPS de poder = mucha principal, Versatilidad y Maestría (golpes grandes y parejos); DPS de crítico = Crítico y Celeridad (picos); sanador de ráfaga = Intelecto, Crítico y Maestría (curas grandes de golpe); sanador sostenido = Voluntad, Celeridad y Versatilidad (curas por ronda que no se acaban) / cambia alguno.

BLOQUE A2 · Oficios y granja (repaso del 2-oct, documento diseno/07-economia/oficios-repaso-2-oct.md)
E-137 (P-136) Arcos y bastones, ahora que la Carpintería hace herramientas: una 🏹 Arquería nueva para arcos y ballestas, y los bastones y varitas al Encantamiento (recomendado) / se quedan en la Carpintería.
E-138 (P-137) Refinar antes de la 3.ª o 4.ª etapa del asentamiento: el Claro conserva estaciones básicas (tablón, lingote, tela, cuero, extracto, sillar) y las variedades piden las estructuras (recomendado) / no se refina nada hasta tener la estructura.
E-139 (P-138) Los rangos que los jugadores ya ganaron en Aserradero, Fundición, Destilación, Tejeduría, Curtiduría y Cantería: se vuelven experiencia de trabajador de esa estructura, nadie pierde nada (recomendado) / se devuelven de otra forma.
E-140 (P-139) Trabajar en una estructura: activo, tocas el botón y gastas energía como hoy al fabricar (recomendado; los empleados del reino, más adelante, trabajan solos) / pasivo, te asignas unas horas y produce solo.
E-141 (P-140) El 🗡️ Ladrón o bandido: ¿es la casa de los bandidos (E-68)? Recomendado: sí; el oficio entra ya robando bolsas de campamentos de monstruos y cofres cerrados, y a jugadores cuando haya PvP / otra idea.
E-142 (P-141) Sueldo de quien trabaja en una estructura: el reino paga por pieza desde su tesoro (recomendado) / por hora / lo fija el monarca.
E-144 (P-143) ¿Quién usa las estructuras de refinado? Los miembros gratis y los visitantes pagando una tarifa al asentamiento (recomendado, D-140) / solo los miembros.
E-145 (P-144) Variedad de los recolectores: tres niveles por recurso (común, del terreno y raro), con 1 a 3 especies por terreno (por ejemplo, roble y abedul en el bosque, caoba y ébano en la selva) (recomendado) / otra forma.
E-146 (P-145) Nodos: cada recolector mejora los nodos de su recurso (Leñador la madera, Minero las menas, Herbolario las hierbas), en vez del carpintero de D-168 (recomendado) / otra.
E-147 (P-146) Herramientas que hace el carpintero: con herramienta rindes más en lo común y la necesitas para lo raro (recomendado) / solo dan un bono / son obligatorias siempre.
E-148 (P-147) ¿Las herramientas se gastan? Sí, como el equipo (E-70) (recomendado) / no se gastan.
E-150 (P-149) 🌾 Agricultura: cultivos para empezar: trigo, lino, algodón, hortalizas, frutas y hierbas cultivadas, solo en las tierras del asentamiento (recomendado) / también en cualquier zona del mapa.
E-151 (P-150) 🐄 Ganadería: animales para empezar: gallinas, ovejas, cabras, vacas y cerdos; caballos y monturas más adelante (recomendado) / otra lista.
E-152 (P-151) Miel y cera de abejas: ¿parte de la Ganadería (recomendado) o de la Agricultura?
E-155 (P-154) Lo que produce la granja es solo del asentamiento: despensa, mantenimiento y obras; los jugadores lo obtienen trabajando o comprando (recomendado) / los miembros pueden sacar.
E-156 (P-155) Tierras para cultivar y criar: cada zona del territorio tiene una fertilidad al azar; más territorio, más tierras (recomendado) / todas las zonas iguales.
E-157 (P-156) Amuletos: los que ya hizo la Joyería quedan de quien los tiene, y desde el cambio los hace la Alquimia (recomendado) / otra cosa.
E-158 (P-157) ✨ Encantamiento como oficio de fabricación: además de encantar y desencantar, ¿crea objetos con esencias (bastones, varitas, runas)? Sí (recomendado) / solo encanta y desencanta.
E-159 (P-158) Especializaciones de los oficios nuevos (Ladrón, Arquería, Agricultura y Ganadería; el Mallero ya no va, D-208): 3 cada uno, como los demás, y las propone Claude (recomendado) / las dices tú.
E-160 (P-159) Orden de trabajo: primero las etapas del asentamiento con sus estructuras y la granja; después la variedad de recolección y los oficios nuevos (recomendado) / primero los oficios.

BLOQUE A3 · Lo del 2-oct: viaje, caravanas, tutorial, armaduras y comida (documento diseno/02-mundo/caravanas-y-aldeanos.md)
E-161 (P-160) El minuto por cuadro (D-197): ¿fijo o se acelera? Recomendado: fijo por ahora; más adelante las monturas de la Ganadería (caballos, E-151) lo bajan a 30 segundos por cuadro, nunca a cero / fijo siempre / otras mejoras.
E-162 (P-161) Mientras viajas: recomendado, como hoy: puedes mirar todo (mochila, héroe, mapa, dudas) pero no trabajar (explorar, recolectar, cazar, fabricar) hasta llegar / puedes hacer otras cosas mientras viajas.
E-163 (P-162) El encargado (D-203): recomendado: es un cargo que nombra el fundador del asentamiento (en el castillo se vota, D-157), uno por tarea (caravanas, agricultura…); el jugador disponible se retira cuando quiera, salvo en una caravana o tarea ya en marcha, porque su energía ya está comprometida / el encargado es el oficial del gremio / otra idea.
E-164 (P-163) Premio por terminar el tutorial: recomendado: además de lo de hoy por paso (5 🥉 y 20 de experiencia), al terminar los 5 pasos 1 🥈 y una bolsa chica que agranda la mochila / solo lo de cada paso / otro premio.
E-165 (P-164) Valores de energía (D-197, D-202): recomendado: nodo chico 1 ⚡ por vuelta (como hoy), mediano 2 y grande 3 (rinden más); caravana: 10 ⚡ más 2 por cuadro de distancia, × 1 chica, × 2 mediana, × 3 grande, repartido entre los escoltas, con escoltas mínimos 2, 4 y 6 / otros números.
E-166 (P-165) El 5.º paso, "Aportar al campamento" (D-204), para quien todavía no tiene campamento: recomendado: volver al Claro y aportar parte de lo recolectado y cazado al 🔥 fogón común del Claro (un aporte de práctica que enseña el botón 🤲 Aportar y da el premio del paso; en tu propio campamento, ese botón alimenta a los aldeanos, D-205) / el paso llega cuando fundas tu campamento / otra idea.
E-167 (P-166) Los pasos de hoy después de cazar (🗺️ Mapa, volver al Claro, 🏕️ Campamento, 🧑‍🏫 Entrenador y 👤 Héroe): recomendado: pasan a ser avisos de una sola vez cuando abres esas pantallas por primera vez, y el camino queda con tus 5 pasos y después fundar el campamento / siguen como pasos después del 5.º.
E-169 (P-168) Comida de los aldeanos (D-207): 1 ración por aldeano y día, 3 aldeanos por nivel, la granja da cerca de la mitad, y con hambre no mueren: no trabajan, no crece el asentamiento y tras 3 días se van de a uno. Recomendado: así / cambia números.

BLOQUE B · Asentamiento, castillo y horarios
E-55 (P-78) Mínimo de miembros para pedir castillo. Dijiste de 40 a 50, pero en la beta habrá pocos jugadores. Opciones: 15 durante la beta y 40 desde el lanzamiento (recomendado) / 40 desde ya / otro número.
E-56 (P-79) Para aprobar el castillo, ¿cuántas oleadas seguidas hay que defender y cuántas victorias de cuántos miembros pide la Noche de prueba? Recomendado: 6 oleadas en dos semanas, ganando al menos 4, y una Noche de prueba con 10 victorias de al menos 5 miembros distintos. ¿Está bien o cambias los números?
E-57 (P-80) La casa del inicio: ¿es el primer escalón del asentamiento (la casa crece y se vuelve campamento, aldea, ciudad...) o cada jugador tiene además su propia casa dentro del asentamiento? Opciones: la casa es el primer escalón, compartido por 3 a 5 jugadores (recomendado) / cada uno tiene su casa aparte / las dos cosas.
E-58 (P-81) Etapas del asentamiento (D-200: el número se decide según los jugadores por asentamiento). ¿Cuántos jugadores esperas en un asentamiento en cada etapa? Recomendado: partir del cupo de hoy (2 al fundar y 2 más por nivel: 6 en la aldea, 10 en el pueblo, 14 en la ciudad y 18 en el castillo; con gremio, hasta 30) y que haya una etapa cada vez que el grupo crece un tercio / dime tú cuántos. (Antes propuse 10: casa, campamento, aldea, pueblo, villa, ciudad, fortaleza, castillo, ciudadela y reino.)
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
E-122 (P-121) Ya cambié los nombres de las habilidades que venían de World of Warcraft. Quedan algunos nombres de clases, especializaciones y recursos que también son de WoW: las clases Caballero de la Muerte, Cazador de demonios y Evocador; especializaciones como Reprensión, Sutileza, Forajido, Disciplina, Profano, Aflicción, Viajero del Viento, Maestro Cervecero, Tejedor de Niebla, Estrago, Venganza, Devorador, Devastación, Preservación y Aumentación; y recursos como Poder Sagrado, Vorágine, Poder Astral, Fragmentos de alma, Cargas Arcanas y Locura. Recomendado: cambiarlos también por nombres propios, sin tocar lo que hace cada una (por ejemplo, Caballero Sepulcral, Azotademonios y Heraldo Dragón para las clases) / dime tú los nombres / dejarlos como están.

E-123 (P-122) Recursos de cada terreno (D-180; ya dijiste que el reparto sea bastante al azar, D-185). Para llegar a 10-15 recursos por terreno, propongo que los 6 de hoy (madera, piedra, fibra, hierba, metal y arcilla) sigan en las mismas zonas y cada terreno sume los suyos (en el bosque: resina, corteza, setas, bayas, miel; en el pantano: juncos, nenúfar, musgo...), que sirven para la cocina, la alquimia y los oficios que vienen, y se venden. Así nadie pierde lo que ya conoce de sus zonas. Ya está así en el juego desde la 0.27 (10 por terreno, de 4 a 6 por zona); si eliges otra cosa, se cambia. Recomendado: así / cambiar todo por variedades de cada terreno (roble, pino, granito...) que cuentan como el material de siempre / las dos cosas.
E-124 (P-123) ¿Qué da un nodo de recursos (D-181)? Recomendado: su recurso rinde el doble y se agota más despacio, y a veces da un material raro de su terreno. Lo usa cualquiera que llegue, hasta que existan los nodos mejorados (D-201 y E-146) y los especiales de los expertos (E-78). Ya está así en el juego desde la 0.27 (2 o 3 nodos por tramo, ✨ en el mapa hasta que llegas). ¿Así u otra idea?
E-125 (P-124) Dijiste que el tipo de nodo se descubre al llegar, y el Explorador aprende justo a saber qué hay antes de llegar (D-172). ¿Su Reconocer también descubre los nodos de lejos? Sí, desde el rango 25 de Explorador (recomendado: es su recompensa) / no, siempre hay que llegar.
E-126 (P-125) Cuevas de mazmorra: entendí "2 o 3 por zona" como 2 o 3 por cada tramo de 6 por 6 zonas (antes eran 1 o 2), así que en el mapa de 13 por 13 hay unas 10 a 12, aunque solo ves las que tienes cerca. ¿Así (recomendado), o querías menos: 2 o 3 en todo lo que muestra el mapa?
E-127 (P-126) Nodos de recursos: el tipo se descubre "solo al llegar". Si vas de viaje a una zona lejana y el camino pasa por la zona de un nodo, ¿pasar por ahí cuenta como llegar? Sí, pisar la zona lo descubre aunque sigas de largo (recomendado: tu héroe estuvo ahí; así quedó en la 0.27) / no, solo cuenta la zona donde termina el viaje.
E-128 (P-127) Terrenos nuevos (0.28): agregué 6, cada uno con su color: 🟣 selva, 🟧 sabana, 🟥 volcán (raro y el más peligroso), 🟤 cañón, ⚫ bosque oscuro y 🔵 lago, con enemigos de los terrenos parecidos y sus propios recursos. Para no revolver lo que los jugadores ya conocen, solo cambiaron las piezas que pasaron a ser de un terreno nuevo (unas 3 de cada 10); las demás siguen igual, con sus recursos y sus nodos. ¿Así (recomendado), cambias algún terreno o color, o prefieres que cada vez que agreguemos terrenos se revuelvan todos los colores del mapa (cambian los recursos propios de casi todas las zonas y 1 de cada 3 nodos)?
E-129 (P-128) Dudas (D-191): dijiste que sea "una IA" que, cuando le mencionas algo, te muestra preguntas ya respondidas. Empiezo con un buscador por palabras (escribes "energía" y salen las preguntas sobre energía, cada una con su código, por ejemplo /d07): es gratis e instantáneo. ¿Le sumamos después una IA de verdad que responda con sus palabras? Eso tiene un costo por mensaje. Recomendado: el buscador ahora y la IA después de la beta / IA desde ya / solo el buscador.
E-130 (P-129) Lo que estaba en 📖 Historia (D-190): la campaña del capítulo 1, las facciones y sus encargos del tablón y el diario. Recomendado: la campaña sigue como parte del camino guiado después del tutorial, el tablón de encargos queda en el Campamento y el diario pasa al Héroe / otra idea.
E-131 (P-130) El origen del héroe (soldado desertor, aprendiz de gremio, huérfano de las ruinas...) se elegía al crearlo. Dijiste que al crear solo van el nombre y la clase. Recomendado: el origen se ofrece más adelante en el camino guiado, como un paso opcional, y quien ya lo eligió lo conserva / quitarlo del todo / dejarlo al crear.
E-132 (P-131) Para que el Campamento y el Héroe se vean "ampliados y separados" como en TowerWars, ¿pueden tener hasta 8 botones de 2 en 2 (en vez de 4 con páginas)? Sí (recomendado: ves todas las opciones de una vez) / no, 4 y páginas.
E-133 (P-132) Los jugadores que ya existen, ¿hacen el camino guiado nuevo? Recomendado: quien ya terminó el tutorial viejo se salta los primeros pasos pero recibe los avisos nuevos a medida que desbloquea cosas; los demás empiezan el camino nuevo / todos lo hacen desde el principio.
E-134 (P-133) Tu propio campamento no cabe en 8 botones: lo que pediste (cocinar, investigar, fabricar, entrenador, dudas), más servicios y tablón, y lo de siempre (agrandar, mejoras, despensa, gremio). Lo partí: el campamento muestra lo tuyo con un botón 🏰 Gestionar, y adentro van ⬆️ Agrandar, 🔨 Mejoras, 🌾 Aportar comida y 🛡️ Gremio. Recomendado: así / 🏰 Gestionar primero en vez de al final / sacar ❓ Dudas del campamento (queda /dudas) para que entre uno más.
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

===== TANDA 5 · EL RESTO DEL CUESTIONARIO DE BETA: LEGAL, DATOS Y SEGURIDAD =====
BLOQUE P · Responsable legal, edad y privacidad
C-069 La política de privacidad y las reglas llevan el nombre de un responsable, y eso decide qué ley aplica. ¿Quién figura y desde qué país? Recomendado: tú como persona mientras el juego sea gratis, y una empresa antes de cobrar cualquier cosa / una empresa que ya tienes / crear una empresa ya.
C-070 El juego tiene heridas duras, putrefacción, crimen y, más adelante, apuestas con oro del juego. ¿Qué edad mínima pedimos para jugar? Recomendado: 16 años, confirmados con un botón al empezar y un aviso corto sobre violencia y azar / 13 / 18.
C-072 ¿Hay menores de edad entre tus jugadores? Recomendado: suponer que hay algunos: apuestas con candado de 18 años, heridas sin detalle gráfico y reglas de chat claras / no hay / hay muchos.
C-074 ¿El bot guarda solo el número de cuenta de Telegram, el idioma y los datos del juego, sin nombre real, teléfono ni correo? Recomendado: sí, lo mínimo; el @usuario se guarda solo para soporte y moderación, y nunca se muestra / guardar más.
C-075 En listas, avisos y combates, ¿se ve solo el nombre del héroe y nunca el @ de Telegram? Recomendado: sí, solo el héroe; quien quiera muestra su @ en su perfil / mostrar el @.
C-078 Algunas leyes exigen poder borrar la cuenta; sería la única excepción a guardar el progreso para siempre, porque la pide el propio jugador. ¿Damos un comando para borrarla? Recomendado: sí, con doble confirmación y 30 días para arrepentirse / solo pidiéndolo a soporte.
C-079 ¿El juego manda datos de jugadores a servicios de fuera, como una IA o una herramienta de errores? Recomendado: solo a una herramienta de errores, sin datos que identifiquen al jugador; nada de IA con textos de jugadores sin decidirlo aparte / nada de fuera / también IA.
C-080 ¿Qué datos de los jugadores ven los moderadores voluntarios? Recomendado: solo el nombre del héroe y el mensaje reportado; las cuentas, historiales y baneos, solo tú y los administradores, con registro de quién mira qué / más datos.
C-077 El héroe se guarda para siempre, pero los registros técnicos no tienen por qué. ¿Cuánto tiempo guardamos cada cosa? Recomendado: héroe y progreso para siempre, registros técnicos 90 días y sanciones 2 años / otros plazos.
C-073 La política de privacidad pide un contacto real. ¿Qué correo publicamos para soporte y privacidad? Recomendado: un correo nuevo solo para el juego, además del comando de soporte; no tu correo personal / otro.

BLOQUE Q · Copias, alertas y permisos del bot
C-039 Si algo grave se rompe y no estás, ¿puedo volver a la versión anterior del juego o ponerlo en mantenimiento sin esperar tu permiso? Recomendado: sí a las dos, avisándote enseguida con el motivo; restaurar una copia de datos, que borra progreso, siempre espera tu sí / solo mantenimiento / no, avísame primero.
C-040 Si hay que restaurar una copia de seguridad, ¿cuánto progreso aceptas perder como máximo? Recomendado: una hora: copia cada hora y una diaria que se guarda 30 días / 15 minutos / un día.
C-041 Si Railway falla o se borra el disco del juego, las copias que están adentro se pierden con él. ¿Guardamos una copia diaria fuera de Railway? Recomendado: sí, protegida con clave, en un almacenamiento aparte a tu nombre, y un simulacro de restauración antes de abrir / con las de Railway basta.
C-042 ¿Dónde quieres enterarte si el bot se cae o da errores? Recomendado: un canal privado de Telegram solo para alertas, más un vigilante de fuera que revisa cada minuto que el bot responde / por correo / los dos.
C-047 ¿Alguien más aparte de ti tiene acceso a Railway, a GitHub o a la clave de @LostRealmsbot? Recomendado: solo tú; si entra un colaborador, acceso limitado al repositorio y nunca a las claves / hay otra persona (¿quién?).
C-049 ¿El proyecto satisfied-balance de Railway comparte cuenta, plan o recursos con TowerWars? Si lo comparte, la carga de 500 jugadores podría afectar a TowerWars, que no se toca. Recomendado: si lo comparte, mover Lost Realms a un proyecto propio antes de la beta (con tu permiso); si ya está separado, dejarlo / no sé.
C-035 El repositorio del juego sigue público: cualquiera puede leer el código y los números de balance para hacer trampas o bots. ¿Lo pasamos a privado antes de la beta? Recomendado: sí, privado; Railway sigue publicando los parches igual / seguir público.
C-046 En los grupos, Telegram limita mucho los mensajes del bot. ¿El juego se juega solo por privado? Recomendado: sí, solo por privado; en los grupos oficiales el bot solo publica avisos / también partidas en grupos.
C-043 ¿Quieres cada día un resumen automático con jugadores, errores y economía? Recomendado: sí, diario en tu canal privado: activos, nuevos, errores, monedas que entran y que salen, campamentos y precios clave, con alarma si las monedas suben más del 20 % en una semana / semanal / no hace falta.

BLOQUE R · Trampas y cuentas falsas
C-140 Hoy invitar da energía apenas el invitado crea su héroe, y con cuentas falsas se junta energía en segundos. ¿La energía por invitar se paga cuando el invitado llega al nivel 5? Cambia una parte de D-65. Recomendado: sí, al nivel 5; lo demás de las invitaciones queda igual / como hoy.
C-152 Contra las cuentas que solo sirven para pasar cosas a otra: cuando existan los regalos y la subasta, ¿las cuentas nuevas no pueden regalar monedas ni objetos en sus primeras 72 horas? Recomendado: sí, 72 horas, y el oro inicial sigue bajo (10 de bronce) / todo abierto.
C-141 En toda beta aparece algún error que duplica monedas u objetos. ¿Se premia a quien lo reporta y se castiga a quien lo aprovecha? Recomendado: sí: quien reporta un error confirmado recibe el título «Cazador de errores»; quien lo aprovecha pierde lo ganado y queda suspendido, y si repite, baneo / solo castigo.
C-142 ¿A los bots y granjas de cuentas se les banea directo, sin la escalera de avisos? Recomendado: baneo directo de todas las cuentas vinculadas, siempre después de que una persona lo revise / escalera normal.
C-144 Un duplicado de madrugada puede durar horas sin que nadie lo vea. ¿El juego se pone solo en mantenimiento si detecta muchos errores o movimientos de monedas raros? Recomendado: sí, con aviso inmediato a ti y a un moderador, más un freno que congela solo el comercio si las monedas creadas en una hora se disparan / no.
C-145 Si se descubre un duplicado grave, ¿aceptas volver todo el servidor unas horas atrás? Eso borra el progreso de quien jugó limpio. Recomendado: primero, una corrección puntual con los registros; volver atrás solo con tu sí, si el abuso está muy repartido y se descubre en menos de 24 horas / volver atrás siempre.
C-143 Si un moderador compite con la misma cuenta con la que modera, cualquier victoria suya parece trampa. ¿El staff juega con una cuenta aparte de la que tiene poderes? Recomendado: sí, cuentas separadas y registro de todo uso / la misma cuenta, con registro.

BLOQUE S · Moderación y soporte
C-051 ¿Tienes ya 5 o 6 moderadores de confianza para la beta, repartidos por horario? Recomendado: elegirlos tú entre jefes de gremio y administradores que conoces, cubriendo mañana, tarde y noche, y que jueguen la prueba cerrada; a cambio, un título de staff, nunca monedas ni poder / tengo pocos / no tengo.
C-052 Además de ti, ¿quién será administrador del juego y de los grupos? Un administrador puede banear y dar objetos. Recomendado: tú y 1 o 2 personas de total confianza / solo tú.
C-053 ¿Quién puede sancionar? Recomendado: los moderadores silencian, congelan el comercio y suspenden hasta 24 horas; el baneo definitivo, solo tú o un administrador, todo registrado con el motivo / solo tú / los moderadores con todo.
C-054 ¿Hay forma de apelar una sanción? Recomendado: sí, un comando para apelar, revisado por alguien distinto de quien sancionó, con respuesta en 72 horas / por privado a un administrador / sin apelación.
C-055 ¿Los errores se reportan con un comando dentro del bot? Recomendado: sí, un comando que guarda la hora, la versión y la última pantalla, y los ordena por gravedad / solo en el grupo / un formulario de fuera.
C-056 En Telegram abundan los estafadores que se hacen pasar por administradores. ¿Dónde piden ayuda los jugadores con problemas de cuenta? Recomendado: un comando de soporte que abre un caso, y una regla fija: el staff nunca te escribe primero ni te pide nada / un tema de ayuda en el grupo / por privado a un moderador.
C-057 Cuando alguien pierde progreso por un error o una caída del bot, ¿qué se compensa? Recomendado: se devuelve lo que se pueda comprobar en los registros; el tiempo caído se compensa igual para todos con algo que no infle, como energía o un cosmético, nunca con monedas en masa / una compensación fija / nada.
C-081 ¿Filtramos los nombres de héroes, campamentos y gremios para bloquear insultos y marcas conocidas? Recomendado: sí: lista de palabras prohibidas, reporte con un botón y cambio de nombre obligado por un moderador / solo reporte.
C-082 ¿Hay temas que el juego nunca toca? Ojo: elegiste heridas realistas y duras, con partes del cuerpo perdidas y putrefacción. Recomendado: nada sexual ni de autolesión, sustancias solo de fantasía, y heridas duras pero contadas en tono de novela, sin gore / otra línea.

BLOQUE T · Plan de apertura y parches
C-149 El piloto automático suma contenido nuevo casi cada día, y eso puede atrasar la apertura. Mientras se prepara la beta, ¿se congela lo que entra y las ideas nuevas esperan en una lista? Recomendado: sí: hasta abrir, solo el parche de beta y arreglos; lo nuevo entra en los parches de después / no, seguir sumando.
C-007 ¿Anunciamos una fecha fija para la beta o una ventana aproximada? Recomendado: una ventana aproximada; la fecha exacta solo cuando se cumplan las condiciones de apertura / fecha fija / sin fecha hasta que esté listo.
C-006 ¿Los 500 entran el mismo día o por oleadas? Recomendado: oleadas de unos 150 por día durante 3 días, con el tope de jugadores y la cola / todos el mismo día / oleadas durante varias semanas.
C-024 ¿Cómo elegimos a los jugadores de la prueba cerrada? Recomendado: los eliges tú: veteranos activos, algunos novatos y los futuros moderadores, todos comprometidos a reportar errores / por sorteo / los primeros que se anoten.
C-083 El nombre ya está decidido, pero "Lost Realms" es común en juegos. Antes del anuncio grande, ¿revisamos que no sea la marca registrada de otro juego? Recomendado: sí, una búsqueda rápida en los registros de marcas; si choca, se suma un subtítulo propio en vez de cambiar el nombre / no hace falta.
C-008 Con 500 personas, un sistema con errores tiene que poder apagarse en segundos sin reiniciar el bot. ¿Cada sistema nuevo llega con un interruptor? Recomendado: sí; el PvP y las apuestas arrancan apagados y se prenden de a uno / no.
C-009 Hoy la regla es uno o dos agentes de IA a la vez, para ahorrar. Con 500 jugadores llegan errores y reportes cada día. ¿Cuánto aceptas gastar en IA por semana durante la beta? Recomendado: el primer mes, un agente fijo para errores y otro para contenido, con el tope semanal que pongas y aviso al llegar al 80 % / uno o dos, como ahora / pon tú un tope.
C-063 Cada parche se avisa por privado a todos (D-67), y hoy salen varios parches en un día. Con 500 personas se siente como spam y algunos bloquean el bot. ¿Juntamos los avisos? Recomendado: como máximo un aviso por día, con los parches del día; los arreglos menores, solo en el canal de novedades / uno por parche, como hoy / solo en el canal.

===== TANDA 6 · EL RESTO DEL CUESTIONARIO DE BETA: JUEGO, COMUNIDAD Y OPERACIÓN =====
BLOQUE U · Juego antes de abrir
C-120 Hoy el mercader compra todo lo que le vendan, a la mitad de su precio y sin tope; con 500 personas eso infla las monedas en días. ¿Le ponemos tope? Recomendado: un tope diario por jugador para venderle, desde que abra la subasta entre jugadores, para que el dinero de verdad venga de venderle a otros / sin tope, como hoy / que no compre.
C-151 La subasta tendrá precio mínimo y máximo (D-26), pero al abrir no hay historial de ventas para calcularlos. ¿Usamos precios de referencia puestos a mano el primer mes? Recomendado: sí, con una banda ancha (de la mitad al triple) que desde la tercera semana se calcula sola / sin bandas al principio.
C-110 Cuando un campamento marca a un visitante como hostil, hoy solo le impide pedir unirse. ¿Qué más puede pasar? Recomendado: por ahora, que tampoco use los servicios del campamento; atacarlo llega con el PvP / dejar que lo ataquen ya.
C-108 Subir al nivel 100 tarda unos 2 años y nunca se borra, así que quien entra semanas después queda muy atrás. ¿Le damos una ayuda? Recomendado: más experiencia cerca del Claro mientras tu nivel esté por debajo del promedio del servidor, sin títulos ya entregados / nada.
C-088 La clase es para siempre (D-74). Si en la beta un parche debilita mucho una clase, ¿damos un cambio de clase gratis por única vez? Recomendado: sí, solo en ese caso, conservando nivel y objetos / no, la clase es para siempre.
C-094 Si un parche cambia mucho una especialización, ¿se regala el reinicio de talentos? Recomendado: sí, gratis durante una semana para esa especialización / se paga igual.
C-109 Tu idea del Colapso trae comunidades PNJ con reglas propias para unirse (D-45). Hoy solo existe el Claro, el campamento base de todos. ¿Cuándo llegan las otras? Recomendado: después de la beta; mientras tanto, el Claro hace de comunidad / antes de la beta.

BLOQUE V · Tu comunidad
C-012 ¿De dónde vienen los 500 jugadores? Recomendado: doy por hecho que casi todos vienen de TowerWars; confírmalo / de otra comunidad / una mezcla.
C-013 ¿Esos 500 juegan a diario o son gente registrada que alguna vez jugó? Recomendado: preparar el servidor para 500 a la vez el primer día y contar con 200 a 300 activos por semana después / activos a diario / registrados, con actividad variable.
C-020 ¿Cuánto tiempo al día juega un jugador típico de tu comunidad? Recomendado: diseñar para varios ratos cortos y una sesión de 30 minutos al día; la energía ya frena a quien juega 3 horas / menos de 30 minutos / de 1 a 3 horas / más de 3 horas.
C-021 ¿Qué es lo que más le gusta a tu comunidad de TowerWars? Recomendado: supongo que la guerra de castillos, los gremios y el parte narrado de la batalla; confírmalo y lo subo en la lista / los jefes / el herrero y el mercado / otra cosa.
C-022 ¿De qué se quejaban más los jugadores de TowerWars? Recomendado: supongo que la subida de nivel lenta, los reinicios con repartos desiguales y los números mal explicados; confírmalo o corrígeme / otra cosa.
C-015 ¿TowerWars sigue funcionando igual durante la beta de Lost Realms? Recomendado: que convivan; Lost Realms se presenta como otro juego, no como reemplazo / Lost Realms lo va a reemplazar / no lo sé.
C-016 ¿Los veteranos de TowerWars reciben algo por venir? Recomendado: nada, porque comprobarlo obligaría a cruzar datos con TowerWars, que no se toca / solo un título cosmético pedido a mano / alguna ventaja.
C-018 ¿Las horas fijas de Lost Realms (oleadas, jefes de mundo) esquivan las batallas de TowerWars? Recomendado: sí, dejar al menos una hora entre unas y otras / no importa.
C-030 ¿Te sirve sacar tú mismo los horarios de conexión y las quejas más repetidas de TowerWars y pasármelos? Yo no puedo tocar TowerWars. Recomendado: es opcional: solo si lo sacas tú, sin nombres de usuario / no.

BLOQUE W · Lanzamiento y canales
C-023 El bot avisa los parches solo a quien ya jugó. ¿Abrimos ya un canal de novedades de Lost Realms? Recomendado: sí, con un diario semanal sin fechas exactas y un enlace para anotarse a la prueba cerrada / esperar a tener fecha.
C-058 ¿Abrimos con solo tres espacios de Telegram: canal de novedades, un grupo general con temas y un grupo privado de staff? Los grupos por castillo y por región van en E-51. Recomendado: sí, esos tres, con temas de general, ayuda, errores, ideas y comercio, y modo lento / varios grupos ya.
C-025 Como el progreso no se borra, el premio a los primeros tiene que ser solo de prestigio. ¿Quien juega la primera semana de la beta, y quien ya jugaba antes, recibe un título? Recomendado: sí: «Fundador» y un cosmético para la primera semana, y un título propio para los que ya jugaban; nada de monedas, niveles ni objetos / nada.
C-026 ¿Hacemos un evento de apertura con hora fija y una meta común? El Claro ya no crece, así que la meta sería otra. Recomendado: sí, «La Fundación»: cuenta regresiva en el canal y una meta de todos para la primera semana (por ejemplo, destruir cierto número de campamentos enemigos), nombrando a los que más aportaron / abrir sin evento.
C-027 ¿Qué número dice que la beta salió bien? Recomendado: que a las 4 semanas sigan jugando al menos 150 personas por día, que 1 de cada 3 vuelva una semana después de entrar y que no haya caídas de más de una hora / más exigente / otro.
C-029 ¿Cuánto debería tardar un jugador nuevo en llegar a su primer combate? Recomendado: menos de 3 minutos, y el tutorial completo en menos de 10, medido con 5 personas que nunca jugaron / 10 minutos / no importa.

BLOQUE X · Operación durante la beta
C-059 Cada subida reinicia el bot y corta las peleas a medias. ¿Los parches grandes se suben en días y horas fijos? Recomendado: dos días fijos por semana, a la hora con menos jugadores y avisando una hora antes; los arreglos urgentes, cuando hagan falta / cualquier día de madrugada / cuando estén listos.
C-060 Si el bot se cae de noche y el reinicio automático no lo arregla, ¿está bien que se arregle a la mañana? Recomendado: sí, con el mundo en pausa y una alerta que veas al despertar; las primeras 72 horas, vigilancia más cercana / no, enseguida.
C-061 ¿En qué horario vas a estar disponible para atender la beta? Recomendado: publicar dos franjas fijas al día; fuera de ellas atienden los moderadores y, si pasa algo grave, el juego queda en mantenimiento hasta la siguiente franja / dime tu horario.
C-062 ¿La IA puede leer los reportes de errores y arreglar sola los menores? Recomendado: sí: los ordena, arregla sola textos y botones rotos, y te pregunta antes de tocar balance, economía o datos de jugadores / solo que los ordene / no, los veo yo.
C-010 Si el mundo no se borra, ¿qué marca el paso de la beta a la versión 1.0? Recomendado: llega cuando entran los sistemas grandes (asentamiento por etapas y castillo, subasta entre jugadores, mazmorras de grupo) y la tienda de cosméticos; solo cambia la etiqueta y nadie pierde nada / por fecha / sin etiqueta de beta.
C-064 El juego premia el robo, la traición y las recompensas por cabezas. ¿Dónde está la línea entre ser un villano del juego y acosar a una persona? Recomendado: robar, traicionar o poner recompensas es parte del juego; los insultos personales, las amenazas reales, perseguir a alguien por privado o publicar sus datos, no / otra línea.
C-065 ¿Hacemos encuestas a los jugadores? Recomendado: sí, una encuesta de Telegram por semana en el canal, de 1 a 3 preguntas / solo al cerrar cada etapa / no.
C-076 Si el bot pasa mensajes entre jugadores, ve lo que escriben. ¿Los guarda? Recomendado: no, solo los pasa; un mensaje se guarda solo si alguien lo reporta, y por 90 días / guardar todo.

BLOQUE Y · Salud, combate y mundo
C-099 Elegiste heridas realistas y duras. Cuando lleguen, ¿qué tan seguido sale una? Recomendado: leve en 1 de cada 4 o 5 peleas, moderada casi solo al caer y grave solo con jefes, medido en la prueba cerrada / más seguido / menos seguido.
C-101 Con una herida, ¿el héroe puede seguir recolectando y viajando? Recomendado: sí: la herida solo castiga lo que usa esa parte del cuerpo; con una pierna herida viajas más lento, pero nunca te quedas sin nada que hacer / la herida bloquea todo.
C-153 Las heridas graves piden un médico jugador, y al principio no habrá. ¿La sanadora PNJ del Claro las trata mientras tanto? Recomendado: sí, cara y lenta, como precio techo, y deja de atenderlas cuando haya unos 5 médicos jugadores activos / no, solo jugadores.
C-154 Las enfermedades las cura el alquimista (D-167). ¿Las clases sanadoras también pueden quitarlas? Recomendado: no; las clases solo limpian efectos de la pelea, como venenos y maldiciones del combate / sí, las leves.
C-132 Hoy hay un solo Guardián de región, Raigambre. ¿Cada cuánto llega uno nuevo en otra parte del mapa? Recomendado: como máximo uno por semana, y el siguiente siempre listo y probado antes / uno cada 2 semanas / sin ritmo fijo.
C-137 La guerra de castillos llega más adelante. ¿Metemos antes una competencia simple entre gremios? Recomendado: sí, una carrera semanal entre gremios (por ejemplo, oleadas defendidas y campamentos enemigos destruidos) / no, esperar.
C-117 En el castillo se vota todo (D-157). ¿Las votaciones se hacen por privado en el bot o con encuestas en el grupo? Recomendado: por privado en el bot, un voto por jugador activo; el grupo solo muestra el resultado / encuesta en el grupo.
C-066 Alguien puede ganar una votación para subir los impuestos al máximo o bloquear a un rival. ¿El equipo del juego puede anular una ley que rompe el juego? Recomendado: sí, un veto de emergencia usado poco y anunciado con el motivo, más límites fijos que nadie puede pasar / no.
C-125 Hoy el mercader solo vende pociones, vendas y provisiones; el equipo sale del botín y de los artesanos. ¿Debería vender también equipo básico? Recomendado: sí, solo lo básico y caro, como red de seguridad cuando faltan artesanos / no, que siga sin equipo.

BLOQUE Z · Nombres y para más adelante
C-155 El PvP usa marcas verde, naranja y roja (D-149) y el crimen usa la Infamia (D-30). ¿Son la misma barra? Recomendado: una sola barra, la Infamia, que pinta el nombre de verde, naranja o rojo / dos separadas.
C-156 La palabra "Profundidades" nombra tres cosas distintas en el diseño. ¿Con cuál se queda? Recomendado: con las mazmorras profundas por pisos (D-170); la zona más peligrosa pasa a llamarse "Tierras Negras" y la dificultad con ese nombre desaparece / otra.
C-159 En el diseño hay tres escalas de dificultad distintas. ¿Usamos una sola para todas las mazmorras? Recomendado: sí: Normal, Heroica, Mítica y Mítica+, y además la dificultad sube con el tamaño del grupo (D-164) / dejarlas como están.
C-084 Cuando entren las apuestas (solo con oro del juego), ¿piden confirmar 18 años o más? Recomendado: sí, un botón de "tengo 18 o más" la primera vez que alguien entra a apostar; quien no lo confirma juega todo lo demás / basta la edad general.
C-157 Telegram no dice de qué país es cada jugador, y alguna ley podría pedir apagar las apuestas en un país. ¿Se lo preguntamos? Recomendado: sí, la primera vez que entra a apostar, con la opción "prefiero no decir" / no.
C-085 Lo que crean los jugadores (misiones, libros, emblemas), ¿lo puede usar y editar el juego? Recomendado: sí: el autor conserva el crédito, y el juego puede usarlo, editarlo y retirarlo / no.

FORMATO DEL RESUMEN FINAL (escríbelo así, sin nada más antes ni después):
RESPUESTAS LOST REALMS · SISTEMA DE PREGUNTAS
E-03: [opción elegida o respuesta corta] | [detalle o condición, si dijo algo más]
E-10: ...
(una línea por cada pregunta que alcanzamos a ver, en este orden: E-03, E-10, E-52, E-171, E-172, E-173, E-174, E-175, E-176, E-182, E-186, E-177, E-178, E-179, E-180, E-181, E-194, E-187, E-188, E-189, E-190, E-191, E-192, E-193, E-137, E-138, E-139, E-140, E-141, E-142, E-144, E-145, E-146, E-147, E-148, E-150, E-151, E-152, E-155, E-156, E-157, E-158, E-159, E-160, E-161, E-162, E-163, E-164, E-165, E-166, E-167, E-169, E-55, E-56, E-57, E-58, E-59, E-60, E-61, E-62, E-63, E-64, E-65, E-66, E-67, E-68, E-69, E-70, E-71, E-72, E-74, E-83, E-84, E-85, E-86, E-87, E-88, E-89, E-90, E-91, E-92, E-93, E-94, E-95, E-97, E-75, E-76, E-78, E-79, E-80, E-81, E-82, E-122, E-123, E-124, E-125, E-126, E-127, E-128, E-129, E-130, E-131, E-132, E-133, E-134, E-44, E-45, E-46, E-47, E-48, E-49, E-50, E-51, E-53, E-54, E-98, E-99, E-100, E-101, E-102, E-103, E-104, E-105, E-106, E-107, E-108, E-109, E-110, E-111, E-112, E-113, E-114, E-115, E-116, E-117, E-118, E-119, E-120, E-121, C-001, C-000, C-003, C-004, C-033, C-034, C-032, C-050, C-011, C-068, C-067, C-069, C-070, C-072, C-074, C-075, C-078, C-079, C-080, C-077, C-073, C-039, C-040, C-041, C-042, C-047, C-049, C-035, C-046, C-043, C-140, C-152, C-141, C-142, C-144, C-145, C-143, C-051, C-052, C-053, C-054, C-055, C-056, C-057, C-081, C-082, C-149, C-007, C-006, C-024, C-083, C-008, C-009, C-063, C-120, C-151, C-110, C-108, C-088, C-094, C-109, C-012, C-013, C-020, C-021, C-022, C-015, C-016, C-018, C-030, C-023, C-058, C-025, C-026, C-027, C-029, C-059, C-060, C-061, C-062, C-010, C-064, C-065, C-076, C-099, C-101, C-153, C-154, C-132, C-137, C-117, C-066, C-125, C-155, C-156, C-159, C-084, C-157, C-085; "sin respuesta" si se saltó; "recomendación" si dijo "lo que recomiendes"; las que no alcanzamos a ver, no las pongas)
HASTA DÓNDE LLEGAMOS: [el último código que vimos]
DUDAS: [lo que preguntó y no supiste responder]
IDEAS SUELTAS: [cualquier idea que dijo fuera de las preguntas]
```
