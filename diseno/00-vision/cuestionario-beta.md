# Cuestionario de beta

> **Módulo** [00 · Visión](README.md) · **Depende de:** [Decisiones](decisiones.md), [Preguntas abiertas](preguntas-abiertas.md) · **Alimenta a:** [Hoja de ruta](hoja-de-ruta.md) · **Estado:** para que responda el dueño (D-39)

Lo que el dueño tiene que responder antes de abrir la beta a más de 500 jugadores. Lo armaron 9 agentes que leyeron el diseño y el juego en vivo, cada uno desde un ángulo distinto. Después se unificaron las preguntas repetidas y un revisor sacó las que ya no aplican: las que suponían pisos, 4 clases o una beta que se borra.

**Cómo responder:** por voz, con el número (por ejemplo "C-001 sí" o "C-004, la segunda"). Cada pregunta trae una recomendación. Basta con decir "de acuerdo con todo menos…". Las respuestas se registran como decisiones (D-xx).

## Resumen

El juego ya está en vivo: Lost Realms 0.6 corre en @LostRealmsbot con 15 clases, talentos, combate, exploración, recolección, campamentos, obra común del Claro y, desde la 0.6, equipo y botín. Lo que no está listo es lo necesario para recibir a 500 personas a la vez. Hoy el bot no tiene herramientas de administración, ni copias de seguridad probadas, ni modo mantenimiento, ni tope de jugadores con cola, y las metas de la obra común son fijas, así que 500 jugadores las terminarían en uno o dos días. Lo más urgente es confirmar que la base de datos está en un volumen de Railway: el código la guarda en la carpeta data/ si no se le indica otra ruta, y sin volumen cada parche borraría a todos los jugadores, cosa que la D-64 prohíbe. Mi recomendación es un parche de beta de 2 a 4 semanas y después una prueba cerrada de 30 a 50 personas. Recién entonces se abre a los 500, por oleadas y con una lista fija de condiciones. Saqué las preguntas que daban por hecho que no había código (pisos, 4 clases, beta que se borra), porque lo que está en vivo y las decisiones confirmadas mandan.

**Nota de hoy (1-oct-2026):** después de este cuestionario, el dueño ya decidió:
- energía de 50, con 40 al día;
- viajes de 2, 2, 3, 3… minutos;
- 100 niveles lentos;
- cinco monedas;
- campamentos que crecen (D-78, D-80 y D-81).

Las preguntas que choquen con eso quedan respondidas por esas decisiones.

## Primera tanda (responder primero)

**C-031. ¿Puedes confirmar en Railway que el servicio RPGDungeon tiene un volumen y que RPG_DB_PATH apunta a él?** · 🔴 bloqueante

✅ Ya está: el servicio RPGDungeon tiene el volumen `lostrealms-data` montado en `/data`, y `RPG_DB_PATH=/data/lostrealms.sqlite3`. Los parches no borran a los jugadores.

**C-001. ¿Los 500 entran al mismo @LostRealmsbot que ya funciona, y ese mundo es el definitivo, sin borrado?** · 🔴 bloqueante

- *Por qué importa:* La D-64 dice que el progreso se guarda para siempre. Entonces los errores de balance se corrigen con ajustes y devoluciones, nunca con un reinicio, y quien entra primero conserva su ventaja. Hay que decirlo en el anuncio.
- *Opciones:* Sí, mundo definitivo · Prefiero un mundo de beta que se borre
- *Recomiendo:* Sí: un solo mundo, el actual, sin borrado. Se anuncia como 'acceso anticipado': los números se ajustan, pero nadie pierde su héroe.

**C-000. ¿Invitamos a los 500 con lo que ya tiene el juego (versión 0.6), o esperamos a un parche de beta?** · 🔴 bloqueante

- *Por qué importa:* El juego ya está en @LostRealmsbot, pero faltan moderación, copias de seguridad, modo mantenimiento, tope de jugadores y una meta común que aguante a 500 personas. Abrir sin eso arriesga perder datos o comunidad.
- *Opciones:* Abrir ya · Esperar al parche de beta · Abrir a una parte ya
- *Recomiendo:* Esperar a un parche de beta de 2 a 4 semanas con lo mínimo: herramientas de administración, copias probadas, mantenimiento, tope con cola y obras que crezcan según la gente. Mientras tanto, anunciar sin fecha exacta.

**C-002. ¿El parche de beta suma solo esto: obra del Claro que crece según la gente, mercado entre jugadores, un primer Guardián cerca del Claro y heridas leves?** · 🔴 bloqueante

- *Por qué importa:* Elegir pocas piezas nuevas decide cuánto tarda la beta. Meter oficios, salud completa y gobierno la atrasa meses.
- *Opciones:* Sí, ese mínimo · Agregar un oficio de fabricación · Agregar más cosas
- *Recomiendo:* Sí, solo eso más las herramientas de administración. Oficios, enfermedades, casas y gobierno llegan durante la beta, un parche cada 2 o 3 semanas (D-60).

**C-003. ¿Aceptas que la beta se abra solo cuando se cumpla una lista fija de condiciones, aunque eso mueva la fecha?** · 🔴 bloqueante

- *Por qué importa:* Así queda claro qué significa 'listo para beta' y no se abre por presión con 500 personas mirando.
- *Opciones:* Sí, con esa lista · Sí, pero cambio condiciones · No, manda la fecha
- *Recomiendo:* Sí. Condiciones: una semana de prueba cerrada sin perder datos, una copia de seguridad que ya se probó restaurar, una prueba de carga con 600 jugadores simulados sin caídas, herramientas de moderación listas y ningún error grave abierto.

**C-004. Antes de abrir a los 500, ¿hacemos una prueba cerrada de 1 a 2 semanas con 30 a 50 jugadores de confianza en @LostRealmsbot?** · 🔴 bloqueante

- *Por qué importa:* Los errores graves (datos perdidos, oro duplicado, bot caído) cuestan poco con 40 personas y mucho con 500. Por la D-64 esa prueba no se borra, así que sus jugadores empiezan con algo de ventaja.
- *Opciones:* Sí, 30 a 50 · Más grande, de 100 · No, directo a los 500
- *Recomiendo:* Sí, con 30 a 50 personas en el bot real y sin borrar nada. Lo arriesgado se prueba en el bot de pruebas aparte. La ventaja es chica porque la experiencia sube lento.

**C-033. ¿Usamos @thetowerwarbot, que quedó libre, como bot de pruebas con su propia base de datos?** · 🔴 bloqueante

- *Por qué importa:* Como el mundo real no se puede borrar (D-64), las pruebas de carga, los ensayos de parches grandes y las pruebas peligrosas necesitan un bot aparte con datos que sí se puedan borrar.
- *Opciones:* Sí, @thetowerwarbot · Creo otro bot · Sin bot de pruebas
- *Recomiendo:* Sí: @thetowerwarbot como bot privado de pruebas, con base propia. Todo parche grande pasa por ahí antes de llegar a @LostRealmsbot.

**C-034. ¿Me das permiso para crear en Railway un servicio aparte para el bot de pruebas, con su propio volumen?** · 🔴 bloqueante

- *Por qué importa:* Hoy solo tengo permiso para el servicio RPGDungeon (D-63). Sin otro servicio, el bot de pruebas no tiene dónde correr.
- *Opciones:* Sí · No, lo creo yo a mano
- *Recomiendo:* Sí, solo ese servicio nuevo, en el mismo proyecto y sin tocar ningún otro.

**C-032. Desde la beta, ¿sigue el piloto automático que despliega solo cada parche, o apruebas tú los parches grandes?** · 🔴 bloqueante

- *Por qué importa:* Con la D-63, cada parche probado se publica solo. Con 500 jugadores, cada despliegue reinicia el bot, y un parche que cambia números o datos sin revisión puede romper la economía de todos.
- *Opciones:* Todo automático · Apruebo los grandes · Apruebo todos
- *Recomiendo:* Los arreglos chicos y urgentes siguen solos, con aviso inmediato para ti. Los parches que tocan balance, datos guardados o sistemas nuevos pasan por el bot de pruebas y esperan tu 'sube'.

**C-050. ¿Aceptas este mínimo de herramientas de moderación para el primer día: reportar, ver transferencias, congelar comercio, suspender, banear y devolver objetos?** · 🔴 bloqueante

- *Por qué importa:* Hoy el bot no tiene ninguna herramienta de administración. Lo que no esté construido antes de abrir no se podrá hacer.
- *Opciones:* Ese mínimo · Menos: solo banear · Más: filtro de chat propio
- *Recomiendo:* Sí, todo con registro de quién hizo qué. El spam de los grupos lo maneja un bot antispam conocido.

**C-011. Hoy cualquiera entra al bot con /start: ¿lo dejamos abierto en la beta?** · 🔴 bloqueante

- *Por qué importa:* Abierto deja entrar curiosos, multicuentas y bots, y no controlas cuánta gente llega. Cerrarlo con códigos choca con las invitaciones que dan energía (D-65).
- *Opciones:* Abierto · Cerrado con códigos · Lista de espera
- *Recomiendo:* Abierto, para que las invitaciones sigan funcionando, pero con tope de jugadores a la vez, cola y reglas contra multicuentas.

**C-103. ¿Las obras del Claro crecen según cuántos jugadores activos hay?** · 🔴 bloqueante

- *Por qué importa:* Hoy las metas son fijas: pasar a Aldea pide 300 de madera y a Ciudad 1.500. Con 500 personas recolectando, el Claro llegaría a Castillo en uno o dos días.
- *Opciones:* Sí · No, metas fijas
- *Recomiendo:* Sí: cada etapa se calcula según los jugadores activos de los últimos 3 días, con un mínimo y un máximo. El avance se ve en el Campamento.

**C-068. ¿Cada jugador acepta con un botón, al entrar, unas reglas cortas?** · 🔴 bloqueante

- *Por qué importa:* Sin reglas aceptadas no hay base para sancionar ni queda escrito que el oro no vale dinero real.
- *Opciones:* Sí, con botón · Solo fijadas en el grupo
- *Recomiendo:* Sí, unas 10 líneas: el oro y los objetos no tienen valor real; está prohibido venderlos o vender cuentas por dinero, usar bots o macros y aprovechar errores; una cuenta por persona; respeto en el chat; sanciones escalonadas. Los jugadores actuales las aceptan al volver a entrar.

**C-067. ¿@LostRealmsbot tiene una política de privacidad propia, o usa la que pone Telegram por defecto?** · 🔴 bloqueante

- *Por qué importa:* La de Telegram no cubre lo que guarda el juego (partidas, reportes, datos contra trampas). Hay que tener una propia antes de invitar a 500.
- *Opciones:* Tengo una propia · Es la de Telegram · No sé
- *Recomiendo:* Redactar una propia, corta y en español, y cargarla en BotFather antes de la prueba cerrada.

## Todas las preguntas, por tema

### Alcance y calendario (11)

**C-000. ¿Invitamos a los 500 con lo que ya tiene el juego (versión 0.6), o esperamos a un parche de beta?** · 🔴 bloqueante

- *Por qué importa:* El juego ya está en @LostRealmsbot, pero faltan moderación, copias de seguridad, modo mantenimiento, tope de jugadores y una meta común que aguante a 500 personas. Abrir sin eso arriesga perder datos o comunidad.
- *Opciones:* Abrir ya · Esperar al parche de beta · Abrir a una parte ya
- *Recomiendo:* Esperar a un parche de beta de 2 a 4 semanas con lo mínimo: herramientas de administración, copias probadas, mantenimiento, tope con cola y obras que crezcan según la gente. Mientras tanto, anunciar sin fecha exacta.

**C-001. ¿Los 500 entran al mismo @LostRealmsbot que ya funciona, y ese mundo es el definitivo, sin borrado?** · 🔴 bloqueante

- *Por qué importa:* La D-64 dice que el progreso se guarda para siempre. Entonces los errores de balance se corrigen con ajustes y devoluciones, nunca con un reinicio, y quien entra primero conserva su ventaja. Hay que decirlo en el anuncio.
- *Opciones:* Sí, mundo definitivo · Prefiero un mundo de beta que se borre
- *Recomiendo:* Sí: un solo mundo, el actual, sin borrado. Se anuncia como 'acceso anticipado': los números se ajustan, pero nadie pierde su héroe.

**C-002. ¿El parche de beta suma solo esto: obra del Claro que crece según la gente, mercado entre jugadores, un primer Guardián cerca del Claro y heridas leves?** · 🔴 bloqueante

- *Por qué importa:* Elegir pocas piezas nuevas decide cuánto tarda la beta. Meter oficios, salud completa y gobierno la atrasa meses.
- *Opciones:* Sí, ese mínimo · Agregar un oficio de fabricación · Agregar más cosas
- *Recomiendo:* Sí, solo eso más las herramientas de administración. Oficios, enfermedades, casas y gobierno llegan durante la beta, un parche cada 2 o 3 semanas (D-60).

**C-003. ¿Aceptas que la beta se abra solo cuando se cumpla una lista fija de condiciones, aunque eso mueva la fecha?** · 🔴 bloqueante

- *Por qué importa:* Así queda claro qué significa 'listo para beta' y no se abre por presión con 500 personas mirando.
- *Opciones:* Sí, con esa lista · Sí, pero cambio condiciones · No, manda la fecha
- *Recomiendo:* Sí. Condiciones: una semana de prueba cerrada sin perder datos, una copia de seguridad que ya se probó restaurar, una prueba de carga con 600 jugadores simulados sin caídas, herramientas de moderación listas y ningún error grave abierto.

**C-004. Antes de abrir a los 500, ¿hacemos una prueba cerrada de 1 a 2 semanas con 30 a 50 jugadores de confianza en @LostRealmsbot?** · 🔴 bloqueante

- *Por qué importa:* Los errores graves (datos perdidos, oro duplicado, bot caído) cuestan poco con 40 personas y mucho con 500. Por la D-64 esa prueba no se borra, así que sus jugadores empiezan con algo de ventaja.
- *Opciones:* Sí, 30 a 50 · Más grande, de 100 · No, directo a los 500
- *Recomiendo:* Sí, con 30 a 50 personas en el bot real y sin borrar nada. Lo arriesgado se prueba en el bot de pruebas aparte. La ventaja es chica porque la experiencia sube lento.

**C-005. ¿Aceptas mis recomendaciones de las preguntas abiertas y me dices solo las que quieres cambiar?** · 🔴 bloqueante

- *Por qué importa:* Muchas definen cómo se programan el combate, la salud y la economía de la beta. Responderlas una por una por voz tomaría semanas.
- *Opciones:* De acuerdo con todo · De acuerdo salvo algunas · Quiero revisarlas todas
- *Recomiendo:* Sí, 'de acuerdo con todo' salvo las que cambies. Revisa primero las que tocan la beta: P-17, P-18, P-22, P-26, P-53, P-55, P-68, P-69 y P-71.

**C-006. ¿Los 500 entran el mismo día o por oleadas?** · 🟠 antes de la beta

- *Por qué importa:* Entrar juntos es mejor para la obra común. Por oleadas es más seguro para el bot y da tiempo de corregir errores, pero quien llega después encuentra el Claro más avanzado.
- *Opciones:* Todos el mismo día · Oleadas en 3 días · Oleadas durante varias semanas
- *Recomiendo:* Oleadas de unos 150 por día durante 3 días. Las metas que dan título (obras del Claro y primer Guardián) se abren cuando entra la última oleada.

**C-007. ¿Anunciamos una fecha fija para la beta o una ventana aproximada?** · 🟠 antes de la beta

- *Por qué importa:* Una fecha fija obliga a recortar a último momento si algo se atrasa. Una ventana da margen sin dejar a la gente sin horizonte.
- *Opciones:* Fecha fija · Ventana aproximada · Sin fecha hasta que esté listo
- *Recomiendo:* Ventana aproximada. La fecha exacta se da solo cuando se cumplen las condiciones de apertura.

**C-008. ¿Cada sistema nuevo llega con un interruptor para apagarlo sin reiniciar el bot?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 personas, un sistema con errores (mercado, PvP, apuestas) tiene que poder apagarse en segundos sin cortar a todos. Ese interruptor hay que construirlo en el núcleo antes.
- *Opciones:* Sí · No
- *Recomiendo:* Sí. PvP, crimen, apuestas y cisma quedan apagados al abrir y se prenden de a uno cuando el núcleo aguante.

**C-009. ¿Cuántos créditos o agentes de IA aceptas gastar por semana durante la beta?** · 🟠 antes de la beta

- *Por qué importa:* Hoy la regla es uno o dos agentes para ahorrar. Con 500 jugadores llegan errores, reportes y ajustes cada día, y si el gasto no alcanza los arreglos se atrasan.
- *Opciones:* Uno o dos agentes como ahora · Más durante el primer mes · Pon tú un tope
- *Recomiendo:* Durante el primer mes, un agente fijo para errores y otro para contenido, con el tope semanal que tú pongas y un aviso al llegar al 80 %.

**C-010. Si el mundo no se borra, ¿qué marca el paso de la beta a la versión 1.0?** · 🟠 antes de la beta

- *Por qué importa:* Sin borrado, el fin de la beta no es un reinicio. Hay que decir qué cambia para no prometer un 'final' que no existe.
- *Opciones:* Por metas y sistemas · Por fecha · Sin etiqueta de beta
- *Recomiendo:* La 1.0 llega cuando se cumple la meta de la beta y entran los sistemas grandes: ciudad con gobierno, oficios completos y tienda de cosméticos. Solo cambia la etiqueta y nadie pierde nada.

### Jugadores y comunidad (20)

**C-011. Hoy cualquiera entra al bot con /start: ¿lo dejamos abierto en la beta?** · 🔴 bloqueante

- *Por qué importa:* Abierto deja entrar curiosos, multicuentas y bots, y no controlas cuánta gente llega. Cerrarlo con códigos choca con las invitaciones que dan energía (D-65).
- *Opciones:* Abierto · Cerrado con códigos · Lista de espera
- *Recomiendo:* Abierto, para que las invitaciones sigan funcionando, pero con tope de jugadores a la vez, cola y reglas contra multicuentas.

**C-012. ¿De dónde vienen los 500 jugadores: de TowerWars, de otra comunidad o mezclados?** · 🟠 antes de la beta

- *Por qué importa:* Si vienen de TowerWars ya se conocen su idioma, horarios y gustos, y llegan con gremios armados. Si no, hay que averiguarlo desde cero.
- *Opciones:* Casi todos de TowerWars · De otra comunidad · Mezcla
- *Recomiendo:* Doy por hecho que casi todos vienen de TowerWars. Confírmalo y uso esa comunidad como punto de partida.

**C-013. ¿Esos 500 juegan hoy a diario, o son gente registrada que alguna vez jugó?** · 🟠 antes de la beta

- *Por qué importa:* 500 jugadores diarios piden otro servidor, más moderadores y otras metas comunes que 500 registrados de los que quizás entren 150.
- *Opciones:* Activos a diario · Activos a la semana · Registrados, con actividad variable
- *Recomiendo:* Preparar el servidor para 500 a la vez el primer día y contar con 200 a 300 activos por semana después. En la beta se mide el número real.
- *Relacionada con:* P-05

**C-014. ¿Invitamos a la comunidad de TowerWars con un mensaje tuyo en sus grupos y su canal, sin usar @TowerWarsBot?** · 🟠 antes de la beta

- *Por qué importa:* Publicar a mano no toca TowerWars. Un envío masivo desde @TowerWarsBot sí lo tocaría (D-01).
- *Opciones:* Sí, a mano · No avisar por ahí
- *Recomiendo:* Sí: un mensaje escrito y fijado por ti en el grupo y el canal de TowerWars, con el enlace a Lost Realms. Nada de envíos desde @TowerWarsBot ni de cruzar bases de datos.
- *Relacionada con:* P-06

**C-015. ¿TowerWars sigue funcionando igual durante la beta de Lost Realms?** · 🟠 antes de la beta

- *Por qué importa:* Si conviven, los jugadores reparten su tiempo y hay que evitar choques de horario. Si Lost Realms lo va a reemplazar, la gente va a esperar llevarse algo.
- *Opciones:* Sí, conviven · Lost Realms lo va a reemplazar · No lo sé
- *Recomiendo:* Que convivan: Lost Realms se presenta como otro juego, no como reemplazo.

**C-016. ¿Los veteranos de TowerWars reciben algo por venir a Lost Realms?** · 🟠 antes de la beta

- *Por qué importa:* Cualquier ventaja rompe la igualdad de entrada. Además, comprobar quién es veterano obligaría a cruzar datos con TowerWars, que no se toca.
- *Opciones:* Nada · Solo un título cosmético · Alguna ventaja
- *Recomiendo:* Nada. Si más adelante quieres un título cosmético, que se pida a mano, sin conectar nunca las bases de datos.

**C-017. ¿En qué países y zona horaria vive la mayoría de tus jugadores?** · 🟠 antes de la beta

- *Por qué importa:* Define la hora de apertura, de los asaltos al Guardián, de los parches y del mantenimiento. También qué leyes de datos aplican: las de Europa son las más estrictas.
- *Opciones:* Latinoamérica · España · Mezclado · Otro
- *Recomiendo:* Si la mayoría está en Latinoamérica, usar UTC-5 como referencia, citas entre las 19:00 y las 22:00 y mantenimiento de madrugada. Si hay jugadores en Europa, aplicar las reglas de datos europeas a todos.
- *Relacionada con:* P-31

**C-018. ¿Las citas de Lost Realms deben evitar los horarios de batalla de TowerWars?** · 🟠 antes de la beta

- *Por qué importa:* Si los mismos jugadores tienen que elegir entre una batalla de TowerWars y un asalto de Lost Realms, pierden los dos juegos.
- *Opciones:* Sí, evitarlas · No importa
- *Recomiendo:* Sí: dejar al menos una hora entre las citas de Lost Realms y las batallas de TowerWars.
- *Relacionada con:* P-31

**C-019. ¿La beta sale solo en español?** · 🟠 antes de la beta

- *Por qué importa:* Traducir cada texto y cada nota de parche duplica el trabajo justo cuando más cambian las cosas. Depende de cuántos juegan solo en inglés.
- *Opciones:* Solo español · Español e inglés · No sé cuántos juegan en inglés
- *Recomiendo:* Solo español si menos de 1 de cada 5 juega en inglés, con un tema #english en el grupo. Los textos ya están separados del motor, así que el inglés se puede sumar después.
- *Relacionada con:* P-04

**C-020. ¿Cuánto tiempo al día juega un jugador típico de tu comunidad?** · 🟠 antes de la beta

- *Por qué importa:* Con eso se calibra cuánta experiencia da cada pelea, cuánto pide cada obra y qué tan rápido crece el Claro.
- *Opciones:* Menos de 30 minutos · 30 a 60 minutos · 1 a 3 horas · Más de 3 horas
- *Recomiendo:* Diseñar para 4 a 6 ratos cortos y una sesión de 30 minutos al día, sin que quien juega 3 horas saque una ventaja enorme.

**C-021. ¿Qué es lo que más le gusta a tu comunidad de TowerWars?** · 🟠 antes de la beta

- *Por qué importa:* Lo que ya les encanta tiene que llegar pronto a Lost Realms, o van a sentir que se mudaron a un juego peor.
- *Opciones:* La guerra de castillos · Los gremios · Los jefes · El herrero y el mercado
- *Recomiendo:* Supongo que la guerra de castillos, los gremios y el parte narrado de la batalla. Confírmalo y lo subo en la lista de parches.

**C-022. ¿De qué se quejaban más los jugadores de TowerWars?** · 🟠 antes de la beta

- *Por qué importa:* Es la lista de errores que Lost Realms no puede repetir.
- *Opciones:* Subir de nivel era lento · Repartos desiguales tras reinicios · Números mal explicados · Otra cosa
- *Recomiendo:* Supongo que la subida de nivel lenta, los reinicios que dejaron repartos desiguales y los números mal explicados. Confírmalo o corrígeme.

**C-023. ¿Abrimos ya un canal de novedades de Lost Realms?** · 🟠 antes de la beta

- *Por qué importa:* El bot avisa de cada parche (D-67), pero solo a quien ya jugó. Un canal mantiene a los 500 al tanto mientras llega la beta.
- *Opciones:* Sí, ya · Esperar a tener fecha
- *Recomiendo:* Sí: un canal con un diario semanal, sin fechas exactas, y un enlace para anotarse a la prueba cerrada o a la beta.

**C-024. ¿Cómo elegimos a los jugadores de la prueba cerrada?** · 🟠 antes de la beta

- *Por qué importa:* Una prueba de amigos que no reportan errores no sirve. Una de desconocidos puede aprovecharse de los errores.
- *Opciones:* Los elijo yo · Por sorteo · Los primeros que se anoten
- *Recomiendo:* Los eliges tú: veteranos activos, algunos novatos y los futuros moderadores, todos comprometidos a reportar errores.

**C-025. ¿Los jugadores de la primera semana reciben un título de Fundador?** · 🟠 antes de la beta

- *Por qué importa:* Como el progreso no se borra, el reconocimiento tiene que ser solo prestigio. Si da poder u oro, el mundo arranca desigual.
- *Opciones:* Título y cosmético · Nada
- *Recomiendo:* Sí: el título 'Fundador del Claro' y un cosmético para quien juegue la primera semana. Nada de oro, niveles ni objetos.

**C-026. ¿Hacemos un evento de apertura, 'La Fundación', con hora fija y una meta común?** · 🟠 antes de la beta

- *Por qué importa:* Una apertura con un objetivo común junta a la gente en el centro del juego y define qué tiene que estar listo el primer día.
- *Opciones:* Sí, La Fundación · Apertura sin evento
- *Recomiendo:* Sí: cuenta regresiva en el canal y la meta de pasar el Claro de fogata a aldea en la primera semana, nombrando a los que más aportaron.

**C-027. ¿Qué número dice que la beta salió bien?** · 🟠 antes de la beta

- *Por qué importa:* Sin una meta que se pueda medir no se sabe si ajustar, seguir o cambiar de rumbo. También define qué mide el resumen diario.
- *Opciones:* Esa meta · Más exigente · Otra
- *Recomiendo:* Que a las 4 semanas sigan jugando al menos 150 personas por día, que 1 de cada 3 vuelva una semana después de entrar y que no haya caídas de más de una hora.

**C-028. Los que ya juegan hoy van a llegar con ventaja sobre los 500: ¿está bien así?** · 🟠 antes de la beta

- *Por qué importa:* Con la D-64, el progreso de quienes entraron antes se queda. Pueden tener nivel, equipo, campamentos y lugares tomados cuando lleguen los 500.
- *Opciones:* Sí, sin cambios · Darles solo un título · Igualar a todos
- *Recomiendo:* Sí, sin quitarles nada. Reciben un título cosmético de 'Pionero', y los 500 entran con un tutorial que los pone al día rápido.

**C-029. ¿Cuánto debería tardar un jugador nuevo en llegar a su primer combate?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 personas entrando a la vez, los primeros minutos deciden quién se queda. El tutorial con pistas (D-56) tiene que ser corto y no trabarse cuando muchos lo hacen al mismo tiempo.
- *Opciones:* 3 minutos · 10 minutos · No importa
- *Recomiendo:* Primer combate antes de los 3 minutos y tutorial completo en menos de 10. Se mide en el bot de pruebas con 5 personas que nunca jugaron.

**C-030. ¿Te sirve sacar tú mismo los horarios de conexión y las quejas más repetidas de TowerWars y pasármelos?** · 🟡 durante la beta

- *Por qué importa:* Con datos reales se eligen mejor las horas de las citas. Yo no puedo tocar TowerWars ni su base de datos (D-01), así que solo sirve si lo sacas tú.
- *Opciones:* Sí, lo saco yo · No
- *Recomiendo:* Es opcional: solo si lo sacas tú, en un archivo sin nombres de usuario. Si no, uso lo que ya está en las lecciones.

### Bot e infraestructura (19)

**C-031. ¿Puedes confirmar en Railway que el servicio RPGDungeon tiene un volumen y que RPG_DB_PATH apunta a él?** · 🔴 bloqueante

✅ Ya está: el servicio RPGDungeon tiene el volumen `lostrealms-data` montado en `/data`, y `RPG_DB_PATH=/data/lostrealms.sqlite3`. Los parches no borran a los jugadores.

**C-032. Desde la beta, ¿sigue el piloto automático que despliega solo cada parche, o apruebas tú los parches grandes?** · 🔴 bloqueante

- *Por qué importa:* Con la D-63, cada parche probado se publica solo. Con 500 jugadores, cada despliegue reinicia el bot, y un parche que cambia números o datos sin revisión puede romper la economía de todos.
- *Opciones:* Todo automático · Apruebo los grandes · Apruebo todos
- *Recomiendo:* Los arreglos chicos y urgentes siguen solos, con aviso inmediato para ti. Los parches que tocan balance, datos guardados o sistemas nuevos pasan por el bot de pruebas y esperan tu 'sube'.

**C-033. ¿Usamos @thetowerwarbot, que quedó libre, como bot de pruebas con su propia base de datos?** · 🔴 bloqueante

- *Por qué importa:* Como el mundo real no se puede borrar (D-64), las pruebas de carga, los ensayos de parches grandes y las pruebas peligrosas necesitan un bot aparte con datos que sí se puedan borrar.
- *Opciones:* Sí, @thetowerwarbot · Creo otro bot · Sin bot de pruebas
- *Recomiendo:* Sí: @thetowerwarbot como bot privado de pruebas, con base propia. Todo parche grande pasa por ahí antes de llegar a @LostRealmsbot.

**C-034. ¿Me das permiso para crear en Railway un servicio aparte para el bot de pruebas, con su propio volumen?** · 🔴 bloqueante

- *Por qué importa:* Hoy solo tengo permiso para el servicio RPGDungeon (D-63). Sin otro servicio, el bot de pruebas no tiene dónde correr.
- *Opciones:* Sí · No, lo creo yo a mano
- *Recomiendo:* Sí, solo ese servicio nuevo, en el mismo proyecto y sin tocar ningún otro.

**C-035. El repositorio del juego hoy es público: ¿lo pasamos a privado antes de la beta?** · 🟠 antes de la beta

- *Por qué importa:* Cualquiera puede leer las reglas internas, los números de balance y el código, y usarlos para hacer trampas o bots.
- *Opciones:* Privado · Seguir público
- *Recomiendo:* Sí, privado. Railway sigue desplegando igual con el permiso de GitHub que ya tiene.
- *Relacionada con:* P-02

**C-036. ¿Seguimos con SQLite durante la beta o pasamos a PostgreSQL antes de abrir a los 500?** · 🟠 antes de la beta

- *Por qué importa:* Hoy el juego usa SQLite, no PostgreSQL como pedía la P-46. Cambiar de base justo antes de abrir es un riesgo. Quedarse obliga a cuidar mucho las copias, porque todo vive en un solo archivo.
- *Opciones:* Medir y decidir · Migrar ya · Seguir con SQLite
- *Recomiendo:* Medir primero con una prueba de carga de 600 jugadores simulados. Si SQLite aguanta, seguir con él en la beta, con copia cada hora, y migrar cuando llegue la web. Si falla, migrar antes de abrir, probándolo en el bot de pruebas.
- *Relacionada con:* P-46

**C-037. ¿Cuánto puedes gastar al mes en Railway durante la beta?** · 🟠 antes de la beta

- *Por qué importa:* Define el tamaño del servicio, el volumen y si cabe el bot de pruebas. Sin tope, un error puede disparar la factura.
- *Opciones:* Hasta 20 USD · Hasta 50 USD · Hasta 100 USD · Otro monto
- *Recomiendo:* Un tope de 50 USD al mes con alerta al 80 %. Para 500 jugadores lo esperable ronda los 20 a 40 USD.
- *Relacionada con:* P-47

**C-038. ¿Quieres un modo mantenimiento que congele los relojes del juego mientras el bot está en pausa o caído?** · 🟠 antes de la beta

- *Por qué importa:* Viajes, energía y, más adelante, heridas, obras y órdenes del mercado avanzan en horas reales. Si el bot se cae seis horas, la gente pierde cosas sin poder hacer nada.
- *Opciones:* Sí · No
- *Recomiendo:* Sí: un botón de pausa que contesta 'en mantenimiento' a todos y descuenta ese tiempo de los temporizadores.

**C-039. Si algo grave se rompe y no estás, ¿puedo volver a la versión anterior del código o poner el juego en mantenimiento sin esperar tu permiso?** · 🟠 antes de la beta

- *Por qué importa:* Volver atrás o pausar tarda un minuto. Esperar tu respuesta puede dejar a 500 jugadores con un duplicado de oro abierto durante horas.
- *Opciones:* Sí, las dos · Solo mantenimiento · No, avísame primero
- *Recomiendo:* Sí a las dos, avisándote enseguida con el motivo. Restaurar una copia de datos, que borra progreso, sigue esperando tu sí.

**C-040. Si hay que restaurar una copia de seguridad, ¿cuánto progreso aceptas perder como máximo?** · 🟠 antes de la beta

- *Por qué importa:* Eso decide cada cuánto se copia la base. Una copia diaria es barata, pero puede borrar un día entero de juego de 500 personas.
- *Opciones:* 15 minutos · Una hora · Un día
- *Recomiendo:* Una hora como máximo: copia automática cada hora y una diaria que se guarda 30 días.

**C-041. ¿Guardamos una copia diaria de la base de datos fuera de Railway?** · 🟠 antes de la beta

- *Por qué importa:* Si la cuenta de Railway falla o el volumen se borra por error, las copias que están dentro se pierden con él.
- *Opciones:* Sí, fuera de Railway · Con las de Railway basta
- *Recomiendo:* Sí: copia diaria cifrada en un almacenamiento aparte a tu nombre, y un simulacro de restauración antes de abrir.

**C-042. ¿Dónde quieres enterarte si el bot se cae o da errores?** · 🟠 antes de la beta

- *Por qué importa:* Sin alertas te enteras cuando los jugadores se quejan, y con 500 eso puede ser horas después.
- *Opciones:* Canal privado de Telegram · Correo · Ambos
- *Recomiendo:* Un canal privado de Telegram solo para alertas, con el bot adentro, más un vigilante externo que revisa cada minuto que el bot responde.

**C-043. ¿Quieres recibir cada día un resumen automático con jugadores, errores y economía?** · 🟠 antes de la beta

- *Por qué importa:* En la beta hay que ver rápido si la gente se queda, dónde falla el juego y si el oro se infla.
- *Opciones:* Diario · Semanal · No hace falta
- *Recomiendo:* Sí, diario en tu canal privado: activos, nuevos, errores, oro total, oro que entra frente al que sale, avance del Claro y precios clave. Alarma si el oro total sube más del 20 % en una semana.

**C-044. El día de apertura, ¿aceptas un tope de jugadores a la vez, con cola cuando se llene?** · 🟠 antes de la beta

- *Por qué importa:* Telegram deja enviar unos 30 mensajes por segundo en total. Si 500 tocan botones a la vez, el bot deja de responder a todos.
- *Opciones:* Tope con cola · Todos a la vez
- *Recomiendo:* Sí: empezar con unos 200 a la vez y dejar entrar 50 cada pocos minutos, mostrando 'estás en el puesto X'. El tope sube según lo que se mida.

**C-045. ¿La beta es solo en Telegram, y la web y la app llegan después?** · 🟠 antes de la beta

- *Por qué importa:* El motor ya está pensado para tres clientes (D-40, D-41), pero construir la web antes de la beta la atrasa meses.
- *Opciones:* Solo Telegram · También web
- *Recomiendo:* Sí: solo Telegram en la beta y la web después, como propone la P-58.
- *Relacionada con:* P-58

**C-046. ¿En la beta el juego se juega solo por privado, sin partidas dentro de grupos?** · 🟠 antes de la beta

- *Por qué importa:* En los grupos, Telegram limita al bot a unos 20 mensajes por minuto por grupo. Jugar solo por privado es más simple y estable.
- *Opciones:* Solo privado · Privado y grupos
- *Recomiendo:* Sí: el juego, solo por privado. En el grupo oficial el bot solo publica avisos.

**C-047. ¿Alguien más aparte de ti tiene acceso a Railway, a GitHub o al token de @LostRealmsbot?** · 🟠 antes de la beta

- *Por qué importa:* Cada persona con acceso es una puerta más para un error o una filtración de datos de jugadores.
- *Opciones:* Solo yo · Hay otra persona
- *Recomiendo:* Solo tú como dueño. Si entra un colaborador, acceso limitado al repositorio y nunca a las variables secretas.

**C-048. ¿Cada parche que cambia la base de datos se prueba antes sobre una copia de los datos reales?** · 🟠 antes de la beta

- *Por qué importa:* Con el progreso guardado para siempre, un cambio de base que sale mal no se arregla borrando. Probarlo sobre una copia detecta el problema antes de que llegue a los 500.
- *Opciones:* Sí · Solo en parches grandes · No
- *Recomiendo:* Sí: antes de cada parche se hace una copia automática, el cambio se prueba sobre ella en el bot de pruebas y solo después se sube.

**C-049. ¿El proyecto satisfied-balance de Railway comparte cuenta, plan o recursos con TowerWars?** · 🟠 antes de la beta

- *Por qué importa:* Si los dos juegos comparten proyecto o plan, la carga de 500 jugadores nuevos o un error de configuración puede afectar a TowerWars, que no se toca.
- *Opciones:* Está separado · Comparte proyecto · No sé
- *Recomiendo:* Si comparten proyecto, mover Lost Realms a uno propio antes de la beta. Si ya está separado, dejarlo como está.

### Operación y moderación (17)

**C-050. ¿Aceptas este mínimo de herramientas de moderación para el primer día: reportar, ver transferencias, congelar comercio, suspender, banear y devolver objetos?** · 🔴 bloqueante

- *Por qué importa:* Hoy el bot no tiene ninguna herramienta de administración. Lo que no esté construido antes de abrir no se podrá hacer.
- *Opciones:* Ese mínimo · Menos: solo banear · Más: filtro de chat propio
- *Recomiendo:* Sí, todo con registro de quién hizo qué. El spam de los grupos lo maneja un bot antispam conocido.

**C-051. ¿Tienes ya 5 o 6 moderadores de confianza para la beta?** · 🟠 antes de la beta

- *Por qué importa:* 500 personas generan dudas, peleas y reportes a toda hora. Sin moderadores repartidos por horario, todo cae en ti.
- *Opciones:* Sí, tengo nombres · Tengo pocos · No tengo
- *Recomiendo:* Elegirlos tú entre jefes de gremio y admins de TowerWars que conoces, cubriendo mañana, tarde y noche, y que jueguen la prueba cerrada. A cambio, un título de staff, nunca oro ni poder.

**C-052. Además de ti, ¿quién será administrador del juego y de los grupos?** · 🟠 antes de la beta

- *Por qué importa:* Un administrador puede banear y dar oro u objetos. Hay que saber en quién se confía eso y quién te cubre cuando no estás.
- *Opciones:* Solo yo · Yo y 1 o 2 más
- *Recomiendo:* Tú y 1 o 2 administradores de total confianza. Nadie más puede banear del juego ni dar objetos.

**C-053. ¿Quién puede sancionar: solo tú, o también los moderadores?** · 🟠 antes de la beta

- *Por qué importa:* Define los permisos de cada rol en el bot, cuánto trabajo cae sobre ti y cuánto se tarda en frenar a un abusador.
- *Opciones:* Solo yo · Moderadores con límites · Moderadores con todo
- *Recomiendo:* Los moderadores silencian, congelan comercio y suspenden hasta 24 horas. El baneo definitivo lo dan solo tú o un administrador. Todo queda registrado con el motivo.

**C-054. ¿Habrá una forma de apelar una sanción?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 personas habrá sanciones equivocadas. Sin una vía para apelar, las quejas terminan en el grupo general o en tu privado.
- *Opciones:* Sí, con /apelar · Por privado a un administrador · Sin apelación
- *Recomiendo:* Sí: comando /apelar, revisado por alguien distinto de quien sancionó, con respuesta en 72 horas.

**C-055. ¿Los errores se reportan con un comando dentro del bot?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 personas, los reportes sueltos en el chat se pierden y llegan sin datos. Un comando que guarda el contexto hay que construirlo antes.
- *Opciones:* Comando en el bot · Solo en el grupo · Formulario externo
- *Recomiendo:* Sí: /reporte guarda la hora, la versión, la última pantalla y el ID, y lo manda a una cola ordenada por gravedad.

**C-056. ¿Dónde piden ayuda los jugadores con problemas de cuenta?** · 🟠 antes de la beta

- *Por qué importa:* En Telegram abundan los estafadores que se hacen pasar por administradores. Una sola vía oficial protege a los jugadores y ordena al staff.
- *Opciones:* Comando en el bot · Tema #ayuda del grupo · Privado a un moderador
- *Recomiendo:* Comando /soporte que abre un caso, y una regla fija en el canal: 'el staff nunca te escribe primero ni te pide nada'.

**C-057. Cuando alguien pierde progreso por un error o una caída, ¿qué se compensa?** · 🟠 antes de la beta

- *Por qué importa:* Como el progreso es para siempre (D-64), habrá pedidos de devolución. Compensar con oro infla la economía, y devolver con justicia exige un registro de acciones desde el primer día.
- *Opciones:* Restaurar desde el registro · Compensación fija · Nada
- *Recomiendo:* Se devuelve lo que se pueda comprobar en los registros. El tiempo caído se compensa igual para todos con algo que no infle (energía o un cosmético), nunca con oro en masa.

**C-058. ¿Abrimos con solo tres espacios de Telegram: canal de novedades, un grupo general con temas y un grupo privado de staff?** · 🟠 antes de la beta

- *Por qué importa:* Cada grupo extra necesita moderación y divide a la gente. Mientras no haya castillos, un grupo con temas concentra todo.
- *Opciones:* Solo esos tres · Varios grupos
- *Recomiendo:* Sí: canal, grupo general con temas (#general, #ayuda, #errores, #ideas, #comercio) y modo lento de 30 segundos, y grupo de staff. Los grupos por campamento llegan después.
- *Relacionada con:* P-42

**C-059. Durante la beta, ¿los parches grandes se suben en días y horas fijos?** · 🟠 antes de la beta

- *Por qué importa:* Cada subida reinicia el bot, corta combates y pierde los botones que se tocaron durante el reinicio. Con horario fijo nadie pierde peleas a medias.
- *Opciones:* Dos días fijos · Cualquier día de madrugada · Cuando estén listos
- *Recomiendo:* Dos días fijos por semana, a la hora con menos jugadores, avisando una hora antes. Los arreglos urgentes, cuando hagan falta.

**C-060. Si el bot se cae de noche y el reinicio automático no lo arregla, ¿está bien que se arregle a la mañana?** · 🟠 antes de la beta

- *Por qué importa:* Tener a alguien atento las 24 horas es caro, pero las primeras noches de una beta suelen traer sorpresas.
- *Opciones:* Sí, a la mañana · No, enseguida
- *Recomiendo:* Sí, con el mundo en pausa y una alerta que veas al despertar. Las primeras 72 horas, vigilancia más cercana.

**C-061. ¿En qué horario vas a estar disponible para atender la beta?** · 🟠 antes de la beta

- *Por qué importa:* Los jugadores y los moderadores tienen que saber cuándo esperar respuesta y qué pueden resolver solos.
- *Recomiendo:* Publicar dos franjas fijas al día. Fuera de ellas atienden los moderadores, y si pasa algo grave se activa el mantenimiento hasta la siguiente franja.

**C-062. ¿La IA puede leer los reportes de errores y arreglar sola los menores?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 personas, ordenar los reportes a mano es mucho trabajo. Si la IA los clasifica y arregla los simples, tú solo decides los importantes.
- *Opciones:* Sí, los menores · Solo que los ordene · No, los veo yo
- *Recomiendo:* Sí: la IA ordena los reportes, arregla sola textos y botones rotos, y te pregunta antes de tocar números de balance, economía o datos de jugadores.

**C-063. ¿Agrupamos los avisos de parches para mandar como máximo uno por día a cada jugador?** · 🟠 antes de la beta

- *Por qué importa:* La D-67 manda cada parche por privado a todos. Con varios parches seguidos y 500 personas, los avisos se sienten como spam y algunos bloquean el bot.
- *Opciones:* Uno por día · Uno por parche como ahora · Solo en el canal
- *Recomiendo:* Sí: como máximo un aviso por día, que junta los parches del día. Los arreglos menores van solo al canal de novedades.

**C-064. ¿Dónde está la línea entre ser un villano dentro del juego y acosar a una persona?** · 🟡 durante la beta

- *Por qué importa:* El diseño premia el robo, la traición y las recompensas por cabezas. Sin esa línea, los moderadores castigarían juego legítimo o dejarían pasar acoso real.
- *Recomiendo:* Robar, traicionar o poner recompensas es parte del juego. Los insultos personales, las amenazas reales, perseguir a alguien por privado o publicar sus datos, no.

**C-065. ¿Hacemos encuestas periódicas a los jugadores?** · 🟡 durante la beta

- *Por qué importa:* Las opiniones del chat reflejan a los que más hablan. Las encuestas dan números para decidir qué ajustar.
- *Opciones:* Semanal · Solo al cierre de etapas
- *Recomiendo:* Sí: una encuesta de Telegram por semana en el canal, de 1 a 3 preguntas.

**C-066. ¿El equipo del juego puede anular una ley de un gobernador si rompe el juego?** · 🟡 durante la beta

- *Por qué importa:* Alguien puede ganar una elección para subir los impuestos al máximo o bloquear a un rival, y sin veto solo queda esperar a que termine el mandato.
- *Opciones:* Sí, veto de emergencia · No
- *Recomiendo:* Sí: veto de emergencia, usado poco y anunciado con el motivo, más límites fijos que el gobernador no puede pasar.

### Legal, datos y dinero (19)

**C-067. ¿@LostRealmsbot tiene una política de privacidad propia, o usa la que pone Telegram por defecto?** · 🔴 bloqueante

- *Por qué importa:* La de Telegram no cubre lo que guarda el juego (partidas, reportes, datos contra trampas). Hay que tener una propia antes de invitar a 500.
- *Opciones:* Tengo una propia · Es la de Telegram · No sé
- *Recomiendo:* Redactar una propia, corta y en español, y cargarla en BotFather antes de la prueba cerrada.

**C-068. ¿Cada jugador acepta con un botón, al entrar, unas reglas cortas?** · 🔴 bloqueante

- *Por qué importa:* Sin reglas aceptadas no hay base para sancionar ni queda escrito que el oro no vale dinero real.
- *Opciones:* Sí, con botón · Solo fijadas en el grupo
- *Recomiendo:* Sí, unas 10 líneas: el oro y los objetos no tienen valor real; está prohibido venderlos o vender cuentas por dinero, usar bots o macros y aprovechar errores; una cuenta por persona; respeto en el chat; sanciones escalonadas. Los jugadores actuales las aceptan al volver a entrar.

**C-069. ¿Quién figura como responsable legal del juego, y desde qué país?** · 🔴 bloqueante

- *Por qué importa:* Ese nombre va en la política de privacidad y en las reglas, y decide qué ley aplica.
- *Opciones:* Yo como persona · Una empresa que ya tengo · Crear una empresa
- *Recomiendo:* Tú como persona mientras sea gratis. Una empresa antes de cobrar cualquier cosa.

**C-070. ¿Qué edad mínima pedimos para jugar?** · 🔴 bloqueante

- *Por qué importa:* El juego tiene heridas, peleas, crimen y azar simulado, y con menores las reglas de datos son más duras.
- *Opciones:* 13 o más · 16 o más · 18 o más
- *Recomiendo:* 16 años, confirmados con un botón al empezar, con un aviso de una línea sobre violencia y azar.

**C-071. ¿La beta es totalmente gratis, sin pagos con Stars?** · 🟠 antes de la beta

- *Por qué importa:* Cobrar exige soporte de pagos, reembolsos y un módulo que hoy no existe. Y lo que se vende pasa a ser una promesa.
- *Opciones:* Gratis · Solo donaciones · Tienda cosmética
- *Recomiendo:* Sí, gratis, como propone la P-64. Los cosméticos y aceleradores de la D-43 llegan después.
- *Relacionada con:* P-64

**C-072. ¿Hay menores de edad entre tus jugadores?** · 🟠 antes de la beta

- *Por qué importa:* Con menores hay que suavizar los textos de heridas y crimen, poner candado a las apuestas y moderar más.
- *Opciones:* No · Algunos · Muchos · No lo sé
- *Recomiendo:* Suponer que hay algunos: apuestas con candado de 18, heridas sin detalle gráfico y reglas de chat claras.

**C-073. ¿Qué correo publicamos como contacto de soporte y de privacidad?** · 🟠 antes de la beta

- *Por qué importa:* La política de privacidad pide un contacto real, y los pedidos de borrado necesitan un lugar fijo.
- *Recomiendo:* Un correo nuevo solo para el juego, además de /soporte. No tu correo personal.

**C-074. ¿Aceptas que el bot guarde solo el ID de Telegram, el idioma y los datos del juego, sin nombre real, teléfono ni correo?** · 🟠 antes de la beta

- *Por qué importa:* Lo que se guarda define la política de privacidad. Cuanto menos se guarde, menos daño hace una filtración.
- *Opciones:* Sí, lo mínimo · Guardar más
- *Recomiendo:* Sí. El @usuario se guarda solo para soporte y moderación, y nunca se muestra.

**C-075. ¿En rankings, avisos y combates se muestra solo el nombre del héroe y nunca el @ de Telegram?** · 🟠 antes de la beta

- *Por qué importa:* Mostrar el @ expone a los jugadores a mensajes de desconocidos y a acoso.
- *Opciones:* Solo el héroe · Mostrar el @
- *Recomiendo:* Sí, solo el nombre del héroe. Quien quiera puede mostrar su @ en su perfil.

**C-076. ¿El bot guarda los mensajes que los jugadores se escriben entre sí?** · 🟠 antes de la beta

- *Por qué importa:* Si el bot pasa mensajes entre jugadores, ve lo que escriben. Guardarlos o no cambia la política de privacidad y la forma de moderar.
- *Opciones:* No guardar · Solo lo reportado · Guardar todo
- *Recomiendo:* No: solo los pasa. Un mensaje se guarda solo si alguien lo reporta, y por 90 días.

**C-077. ¿Cuánto tiempo guardamos los registros técnicos y de sanciones?** · 🟠 antes de la beta

- *Por qué importa:* Hay que ponerlo en la política. El héroe y su progreso se guardan para siempre (D-64), pero los registros con datos de uso no tienen por qué.
- *Recomiendo:* Héroe y progreso, para siempre. Registros técnicos, 90 días. Sanciones, 2 años.

**C-078. ¿Damos un comando para que un jugador borre su cuenta si lo pide?** · 🟠 antes de la beta

- *Por qué importa:* Muchas leyes de datos lo exigen. Es la única excepción a guardar el progreso para siempre, porque la pide el propio jugador.
- *Opciones:* Sí, con comando · Solo pidiéndolo a soporte
- *Recomiendo:* Sí: /borrarcuenta con doble confirmación y 30 días para arrepentirse. Los registros del mercado quedan sin nombre.

**C-079. ¿El juego enviará datos de jugadores a servicios externos, como una IA o una herramienta de errores?** · 🟠 antes de la beta

- *Por qué importa:* Cada servicio externo va en la política de privacidad y suma riesgo. Mandar textos de jugadores a una IA es lo más delicado.
- *Opciones:* Nada externo · Solo errores · También IA
- *Recomiendo:* Solo una herramienta de errores, con el ID cifrado. Nada de IA con textos de jugadores hasta decidirlo aparte.

**C-080. ¿Qué datos de los jugadores pueden ver los moderadores voluntarios?** · 🟠 antes de la beta

- *Por qué importa:* Los moderadores también juegan. Si ven IDs o historiales ajenos, pueden filtrarlos o sacar ventaja.
- *Recomiendo:* Solo el nombre del héroe y el mensaje reportado. Los IDs, historiales y baneos, solo tú y los administradores, con registro de quién consulta qué.

**C-081. ¿Filtramos los nombres de héroes y campamentos para bloquear insultos y marcas conocidas?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 personas el primer día van a aparecer insultos y nombres de otros juegos, a la vista de todos.
- *Opciones:* Filtro y reporte · Solo reporte
- *Recomiendo:* Sí: lista de palabras prohibidas, reporte con un botón y cambio de nombre forzado por un moderador.

**C-082. ¿Hay temas que el juego nunca debe tocar, como contenido sexual, autolesión o drogas reales?** · 🟠 antes de la beta

- *Por qué importa:* Define cómo se escriben las enfermedades, la mente y el crimen, y protege al bot frente a las reglas de Telegram.
- *Recomiendo:* Sí: nada sexual ni de autolesión, sustancias solo de fantasía y heridas en tono de novela, sin gore.

**C-083. Antes del anuncio grande, ¿revisamos que 'Lost Realms' no sea la marca registrada de otro juego?** · 🟠 antes de la beta

- *Por qué importa:* El nombre ya está decidido (D-62), pero es común en juegos. Cambiarlo después de anunciarlo a 500 personas confunde y puede traer un reclamo.
- *Opciones:* Sí, revisar · No hace falta
- *Recomiendo:* Sí: una búsqueda rápida en los registros de marcas (EUIPO, USPTO, WIPO) antes del anuncio. Si choca, sumar un subtítulo propio en lugar de cambiar el nombre.

**C-084. Cuando entren las apuestas, ¿piden confirmar que el jugador tiene 18 años o más?** · 🟡 durante la beta

- *Por qué importa:* Aunque sea oro del juego, el azar simulado suele tratarse como contenido para adultos.
- *Opciones:* Sí, 18 para apostar · No, basta la edad general
- *Recomiendo:* Sí: un botón de 'tengo 18 o más' la primera vez que alguien entra a apostar. Quien no lo confirma juega todo lo demás.

**C-085. Lo que crean los jugadores (misiones, libros, emblemas), ¿lo puede usar y editar el juego?** · ⚪ después

- *Por qué importa:* El diseño deja que los jugadores escriban contenido que entra al juego con su firma. Sin esa cláusula, un autor podría exigir que se retire.
- *Recomiendo:* Sí: el autor conserva el crédito y el juego puede usar, editar y retirar lo que crea.

### Núcleo del juego (1)

**C-086. El Guardián de región, ¿es una pelea por grupo donde gana el primer grupo que lo mata, o una sola vida compartida por todo el servidor?** · 🟠 antes de la beta

- *Por qué importa:* Con 500 jugadores cambia cómo se programa la pelea, cuántos mensajes manda el bot y quién gana el título de Pionero.
- *Opciones:* Por grupo, en paralelo · Vida compartida del servidor
- *Recomiendo:* Pelea por grupo, en paralelo: el primer grupo que gana es Pionero, y la región pasa a Asentamiento para todos.

### Clases y combate (9)

**C-087. ¿Las 15 clases que ya están en el juego siguen todas disponibles para los 500?** · 🟠 antes de la beta

- *Por qué importa:* Las 15 ya se publicaron y sus IDs no se borran. Mantenerlas todas obliga a revisar con más cuidado el balance de sus especializaciones antes de abrir.
- *Opciones:* Sí, las 15 · Ocultar algunas por ahora
- *Recomiendo:* Sí, las 15. Antes de abrir se pasan todas por el simulador de balance y se ajusta lo que quede muy fuera de rango.

**C-088. La clase es para siempre (D-74): si en la beta una clase se debilita mucho, ¿damos un cambio de clase gratis por única vez?** · 🟠 antes de la beta

- *Por qué importa:* Con números que todavía se mueven, alguien puede quedar atrapado en una clase debilitada, y la regla actual no le da salida. Sería una excepción a una decisión confirmada.
- *Opciones:* Sí, solo en ese caso · No, la clase es para siempre
- *Recomiendo:* Sí, solo cuando un parche debilita mucho una clase: quienes la tienen reciben un cambio gratis y conservan nivel y objetos. Fuera de eso, la clase sigue siendo para siempre.

**C-089. ¿El equipo de la 0.6 (arma, armadura y joya, con requisito de nivel y de tipo) queda así para la beta?** · 🟠 antes de la beta

- *Por qué importa:* Ya está en vivo. Sumar ahora más ranuras, peso o durabilidad agrega trabajo y cambia el balance justo antes de abrir.
- *Opciones:* Queda así · Sumar más ya
- *Recomiendo:* Que quede así. Las 10 ranuras, la carga y la durabilidad llegan con la fabricación (D-44, D-77).
- *Relacionada con:* P-71

> En el juego hoy: el equipo tiene 7 ranuras (arma, cabeza, pecho, manos, piernas, pies y joya) y solo el nivel impide ponerse una pieza; lo que no es de tu clase rinde la mitad (D-83).

**C-090. ¿Cuántos jugadores pueden entrar a la vez contra el Guardián en la beta?** · 🟠 antes de la beta

- *Por qué importa:* El diseño permite de 5 a 25. Una pelea de 25 en un solo mensaje de Telegram nunca se probó y puede romper el ritmo y los límites del bot.
- *Opciones:* 5 a 10 · 5 a 15 · 5 a 25
- *Recomiendo:* De 5 a 10 contra el Guardián. Subir a 25 cuando se prueben las bandas.

**C-091. ¿En cuánto tiempo debería caer el primer Guardián?** · 🟠 antes de la beta

- *Por qué importa:* La meta es una dificultad como la de Elden Ring (D-08), pero es el primer jefe que verán 500 personas. Si nadie lo mata en semanas, la beta se estanca.
- *Recomiendo:* Difícil pero justo: el mejor grupo lo vence tras 2 a 4 días de intentos y un grupo promedio en 1 a 2 semanas. La dificultad completa llega con los Guardianes siguientes.

**C-092. ¿Cuánto dura cada ronda de combate en grupo?** · 🟠 antes de la beta

- *Por qué importa:* Una ronda larga aburre y una corta castiga a quien juega desde el trabajo. También define cuántos mensajes edita el bot por minuto.
- *Opciones:* 30 s · 45 s · 60 s · 90 s
- *Recomiendo:* 45 segundos en grupo, 60 contra el Guardián y sin reloj en solitario. La ronda se cierra en cuanto todos eligieron.
- *Relacionada con:* P-17

**C-093. ¿Basta con una táctica automática fija por especialización para quien no responde a tiempo?** · 🟠 antes de la beta

- *Por qué importa:* El editor de tácticas es un trabajo grande, pero sin ninguna táctica, quien no responde deja un hueco en su grupo.
- *Opciones:* Táctica fija · Editor desde el inicio
- *Recomiendo:* Sí: una táctica fija por especialización. Contra el Guardián, el héroe usa su habilidad defensiva. El editor llega después.
- *Relacionada con:* P-18

**C-094. Cuando un parche cambia mucho una especialización, ¿se regala un reinicio de talentos gratis?** · 🟡 durante la beta

- *Por qué importa:* El progreso no se borra (D-64). Si un ajuste debilita tu especialización, pagar oro para cambiarla se siente injusto.
- *Opciones:* Sí, reinicio gratis · No, se paga igual
- *Recomiendo:* Sí: reinicio de talentos gratis durante una semana para esa especialización.

**C-095. ¿La técnica del arma entra como opción para una de las 3 casillas de habilidad?** · 🟡 durante la beta

- *Por qué importa:* Haría que el arma de un artesano importe en combate, pero cada tipo de arma necesita su técnica y su balance.
- *Opciones:* Sí, catálogo corto · Dejarla para después · Eliminarla
- *Recomiendo:* Sí, con un catálogo corto, cuando llegue la herrería: una técnica por tipo de arma, que el jugador puede poner en lugar de una habilidad.
- *Relacionada con:* P-68

### Salud y muerte (7)

**C-096. ¿Qué tan profunda es la salud al abrir la beta?** · 🟠 antes de la beta

- *Por qué importa:* La salud completa (D-09) es uno de los sistemas más grandes. Hoy solo hay vida, pociones y vendas.
- *Opciones:* Solo pociones, como hoy · Heridas leves · Heridas y enfermedades
- *Recomiendo:* Al abrir, heridas leves por zona del cuerpo que curan solas o con vendas. Las heridas graves, los médicos y las enfermedades simples llegan por parches durante la beta.

**C-097. ¿Qué pierde un jugador al caer en la beta?** · 🟠 antes de la beta

- *Por qué importa:* Es lo que más decide si el juego se siente justo o frustrante. Hoy pierde el 10 % de su oro.
- *Opciones:* Solo el oro, como hoy · Oro y una herida · También saqueo
- *Recomiendo:* Mantener el 10 % del oro y sumar una herida leve cuando lleguen las heridas. Sin saqueo de mochila ni de equipo.

**C-098. ¿Las secuelas definitivas y la muerte permanente quedan apagadas hasta que el balance sea estable?** · 🟠 antes de la beta

- *Por qué importa:* La D-51 confirma secuelas definitivas, pero como el progreso no se borra, perder una pierna o el personaje por un error de números no tiene arreglo justo.
- *Opciones:* Apagadas al principio · Desde que entre la salud
- *Recomiendo:* Sí: al principio, solo cicatrices cosméticas. Las secuelas definitivas y el Juramento de Hierro se prenden cuando la salud lleve semanas estable.
- *Relacionada con:* P-26

**C-099. Cuando lleguen las heridas, ¿qué tan seguido debería salir una?** · 🟡 durante la beta

- *Por qué importa:* Si salen con cada golpe fuerte, medio servidor anda vendado todo el tiempo.
- *Recomiendo:* Leve en 1 de cada 4 o 5 peleas, moderada casi solo al caer y grave solo con jefes. Se mide en la prueba cerrada.

**C-100. ¿Las heridas curan en horas y no en días mientras haya pocos médicos?** · 🟡 durante la beta

- *Por qué importa:* Una herida crítica de 7 días reales deja a un jugador fuera mucho tiempo, justo cuando todavía no hay quién lo cure.
- *Opciones:* Sí, en horas · Tiempos del diseño
- *Recomiendo:* Sí: leve de 1 a 3 horas, moderada de 3 a 12 y grave de 12 a 36. El descanso fuera de línea sigue acelerando la curación.
- *Relacionada con:* P-22

**C-101. ¿Un héroe herido puede seguir recolectando y viajando?** · 🟡 durante la beta

- *Por qué importa:* Si una herida bloquea todo, el jugador no tiene nada que hacer y se desconecta. Si no bloquea nada, no importa.
- *Opciones:* Sí, con penalización · No, bloquea todo
- *Recomiendo:* Sí: la herida solo castiga lo que usa esa parte del cuerpo. Con una pierna herida viajas más lento, pero nunca te quedas sin nada que hacer.

**C-102. Cuando entren las enfermedades, ¿se contagian entre jugadores?** · 🟡 durante la beta

- *Por qué importa:* Sin médicos formados, una epidemia puede tumbar a medio servidor.
- *Opciones:* Sin contagio al principio · Con contagio
- *Recomiendo:* No al principio: 3 enfermedades simples sin contagio. El contagio se prende cuando haya suficientes médicos.
- *Relacionada con:* P-21

### Mundo y fundación (15)

**C-103. ¿Las obras del Claro crecen según cuántos jugadores activos hay?** · 🔴 bloqueante

- *Por qué importa:* Hoy las metas son fijas: pasar a Aldea pide 300 de madera y a Ciudad 1.500. Con 500 personas recolectando, el Claro llegaría a Castillo en uno o dos días.
- *Opciones:* Sí · No, metas fijas
- *Recomiendo:* Sí: cada etapa se calcula según los jugadores activos de los últimos 3 días, con un mínimo y un máximo. El avance se ve en el Campamento.

**C-104. ¿Cuánto deberían tardar los 500 en llevar el Claro hasta Aldea y hasta Castillo?** · 🟠 antes de la beta

- *Por qué importa:* Con este número se calcula cuánto pide cada etapa. Muy rápido y la meta común se acaba; muy lento y la gente se aburre.
- *Opciones:* Más rápido · 7 a 10 días y 4 a 6 semanas · Más lento
- *Recomiendo:* De 7 a 10 días hasta Aldea, y de 4 a 6 semanas hasta Castillo, como propone la P-55.
- *Relacionada con:* P-55

**C-105. ¿Dónde aparece el primer Guardián de región: cerca del Claro o lejos, en la Frontera?** · 🟠 antes de la beta

- *Por qué importa:* Sin pisos (D-58), los jefes están repartidos por el mapa. Si está lejos, con 20 de energía al día muchos no llegan; si está cerca, se vuelve la meta común de las primeras semanas.
- *Opciones:* Cerca del Claro · En un lugar que hay que descubrir · En la Frontera, lejos
- *Recomiendo:* Cerca del Claro, a 3 o 5 zonas. El siguiente tiene que estar listo y probado antes de que caiga el primero.

> En el juego hoy: Raigambre, el primer Guardián, vive en (5, 2), a Lejanía 5 del Claro, y se pelea en solitario. La energía es de 50, con 40 al día (D-78, D-82).

**C-106. ¿El primer Guardián se abre solo cuando el Claro llega a Aldea?** · 🟠 antes de la beta

- *Por qué importa:* Si se abre antes, los que pelean abandonan la obra común. Atarlo a la Aldea hace que todos se necesiten.
- *Opciones:* Sí · No, desde el primer día
- *Recomiendo:* Sí, al llegar a Aldea.

**C-107. Si cientos aportan a la misma etapa del Claro, ¿quién se lleva el título de Fundador de esa etapa?** · 🟠 antes de la beta

- *Por qué importa:* Con cientos aportando, dárselo al primero es injusto o imposible de decidir.
- *Recomiendo:* El título único, para quien más aportó a esa etapa. Todos los que aportaron un mínimo reciben una insignia y su nombre en una placa.

**C-108. ¿Qué recibe quien entra semanas después de abrir?** · 🟠 antes de la beta

- *Por qué importa:* La experiencia sube lento y nunca se borra (D-64), así que quien llega tarde queda muy atrás. Con demasiada ayuda, los primeros sienten que no valió.
- *Opciones:* Viento de Cola · Nada
- *Recomiendo:* El Viento de Cola que ya propone el diseño: más experiencia en las zonas cercanas al Claro mientras tu nivel esté por debajo del promedio. Nada de títulos ya entregados.

**C-109. La D-45 dice que puedes unirte a una comunidad PNJ: ¿en la beta hay comunidades PNJ para unirse?** · 🟠 antes de la beta

- *Por qué importa:* Si las hay, parte de los 500 se queda en ellas y el Claro pierde gente cuando más la necesita.
- *Opciones:* Solo el Claro · Varias para unirse
- *Recomiendo:* En la beta, el Claro hace de comunidad de supervivientes: da el tutorial, enseña lo básico y tiene la sanadora. Las comunidades para unirse llegan después.

**C-110. Cuando alguien marca a un visitante de su campamento como hostil, ¿qué puede pasar?** · 🟠 antes de la beta

- *Por qué importa:* El aviso de amistoso u hostil (D-71) ya existe, pero no está definido si 'hostil' permite atacar. Si lo permite, hay PvP desde el primer día.
- *Opciones:* Solo cerrar servicios · Permite atacar
- *Recomiendo:* Por ahora solo le cierra al visitante los servicios del campamento (posada, mercader y obra). Atacar llega con el PvP, más adelante.

**C-111. Hasta que haya gobernador, ¿quién decide qué obra se construye primero?** · 🟡 durante la beta

- *Por qué importa:* Sin una forma de decidir, 500 personas se pelean o un gremio grande se queda con las obras y el tesoro.
- *Opciones:* PNJ con voto semanal · Orden fijo · Los jugadores libremente
- *Recomiendo:* Un PNJ propone 3 obras cada semana y los jugadores activos votan por privado en el bot. Se retira cuando se elige el primer gobernador.

**C-112. Cuando lleguen las casas, ¿qué casa puede tener un jugador recién llegado?** · 🟡 durante la beta

- *Por qué importa:* Una casa completa exige un rango alto de Construcción, y el primer día nadie lo tiene.
- *Recomiendo:* Un cobertizo básico con cama y baúl que cualquiera puede levantar. Las habitaciones se suman con rango.
- *Relacionada con:* P-43

**C-113. ¿Cómo se reparten las parcelas para casas cuando cientos las quieren a la vez?** · 🟡 durante la beta

- *Por qué importa:* El diseño las subasta con oro, pero al principio nadie tiene oro y el primero que llega acapara.
- *Opciones:* Una por cuenta · Sorteo · Subasta
- *Recomiendo:* Una parcela chica garantizada por cuenta, que se pierde si no se construye en 7 días. Las grandes se subastan más adelante.
- *Relacionada con:* P-43

**C-114. Cuando lleguen los gremios, ¿les ponemos un tope de 25 miembros?** · 🟡 durante la beta

- *Por qué importa:* Los gremios de TowerWars pueden llegar enteros y quedarse con los mejores lugares y con la primera elección.
- *Opciones:* Sí, 25 · Otro tope · Sin tope
- *Recomiendo:* Sí, 25, y elecciones con un voto por jugador activo, nunca por gremio.

**C-115. ¿El Claro puede bajar de etapa si le falta comida, salud o defensa durante varios días?** · 🟡 durante la beta

- *Por qué importa:* Hace difícil la fundación, pero con números sin probar, una caída por un error de balance puede hundir el ánimo de todos.
- *Opciones:* Sí, desde la Aldea · No en la beta
- *Recomiendo:* Sí, desde la Aldea, con avisos claros antes de bajar. Si la caída fue por un error de números, se devuelve.

**C-116. ¿El Claro, que es zona segura, puede sufrir incendios e incursiones que dañen sus edificios?** · 🟡 durante la beta

- *Por qué importa:* Un documento dice que lo construido en zona segura nunca se ataca, y otros traen crisis contra la ciudad.
- *Opciones:* Sí, solo edificios públicos · No, es intocable
- *Recomiendo:* Sí: los edificios públicos se pueden dañar en crisis avisadas, pero nadie cae ni pierde objetos personales.
- *Relacionada con:* P-52

**C-117. ¿Las elecciones se votan por privado en el bot o con encuestas en el grupo?** · 🟡 durante la beta

- *Por qué importa:* Una encuesta de grupo no comprueba que vote un jugador activo: vota cualquiera, incluidas las cuentas vacías.
- *Opciones:* Por privado en el bot · Encuesta del grupo
- *Recomiendo:* Por privado en el bot, un voto por jugador activo. El grupo solo muestra el resultado.

### Economía y oficios (12)

**C-118. ¿Qué oficios llegan primero en los parches de la beta?** · 🟠 antes de la beta

- *Por qué importa:* Hoy solo se recolecta. Cada oficio cuesta mucho diseño y código, y decide qué se puede fabricar y curar.
- *Opciones:* Construcción y Medicina primero · Fabricación primero
- *Recomiendo:* Primero Construcción y Medicina (D-11) y uno de fabricación, Herrería o Carpintería. Los demás, de a uno cada 2 o 3 semanas.

**C-119. ¿Con cuánto oro empieza cada personaje?** · 🟠 antes de la beta

- *Por qué importa:* Hoy empieza con 10 de oro y 5 más por el tutorial. Con 500 cuentas, el oro inicial es lo primero que una cuenta falsa le regala a la principal.
- *Recomiendo:* Mantener esa cantidad baja, y que no se pueda transferir hasta el nivel 5.

**C-120. ¿El mercader del campamento sigue comprando todo lo que le vendan, sin tope?** · 🟠 antes de la beta

- *Por qué importa:* Vender al PNJ es la entrada de oro más fácil de abusar: 500 personas recolectando y vendiendo (ahora también el botín de la 0.6) inflan el oro en días.
- *Opciones:* Con tope diario · Sin tope, como hoy · Que no compre
- *Recomiendo:* Que siga comprando, pero con un tope diario por jugador y precio más bajo. El oro tiene que entrar sobre todo por las obras y los pedidos del Claro.

**C-121. ¿La obra del Claro paga oro a quien aporta, desde un fondo que se acaba?** · 🟠 antes de la beta

- *Por qué importa:* Hoy aportar da experiencia. Pagar oro motiva más, pero es una entrada grande de oro que hay que medir.
- *Opciones:* Sí, hasta la Aldea · No, solo experiencia
- *Recomiendo:* Sí: un fondo fijo del Claro que paga hasta la Aldea y se acaba ahí. Después, las obras se pagan con impuestos.

**C-122. Cuando abra el mercado entre jugadores, ¿cobra 1,5 % por publicar y 4 % por vender?** · 🟠 antes de la beta

- *Por qué importa:* Son la vía principal por la que sale oro del juego. Arrancar sin comisión acostumbra mal; una comisión muy alta ahoga el comercio.
- *Opciones:* Sí · Más bajas al principio
- *Recomiendo:* Sí, desde el primer día del mercado. Más adelante, el gobernador las mueve dentro de un rango fijo.

**C-123. ¿Las 💎 Gemas se consiguen solo jugando, o serán la moneda que se compra con dinero real?** · 🟠 antes de la beta

- *Por qué importa:* Las gemas ya se ven en la ficha (D-76). Si después se venden por dinero, quienes las ganaron jugando sentirán que se les quitó algo, y la D-43 solo permite vender cosméticos y aceleradores.
- *Opciones:* Solo jugando · Jugando y comprando · Solo comprando
- *Recomiendo:* Solo jugando, muy escasas y para lo más valioso. Si algún día hay moneda de pago, que sea otra, con otro nombre.

> En el juego hoy: las gemas pasaron a llamarse 💎 Diamantes y son la moneda que se compra con dinero real, solo para aceleradores y cosméticos (D-80, D-85).

**C-124. Como no hay límite de oficios (D-57), ¿basta el costo de tiempo para que los jugadores se necesiten entre sí?** · 🟠 antes de la beta

- *Por qué importa:* Si una persona puede aprenderlo todo, los 500 juegan cada uno por su lado y el mercado entre jugadores no arranca, que es justo lo que la beta tiene que probar.
- *Opciones:* Solo el costo de tiempo · Sumar otro freno
- *Recomiendo:* Sí: el freno es el tiempo. Cada oficio extra tarda en subir y los materiales vienen de zonas lejanas entre sí. Sin límites duros, como pediste.
- *Relacionada con:* P-69

**C-125. Cuando haya artesanos, ¿los PNJ siguen vendiendo equipo básico?** · 🟡 durante la beta

- *Por qué importa:* Si no venden nada, todo se traba cuando faltan artesanos. Si venden mucho o barato, los artesanos no tienen a quién vender.
- *Opciones:* Sí, caro y básico · No venden nada
- *Recomiendo:* Sí, pero solo lo básico y caro, como precio techo y red de seguridad.

**C-126. ¿Ponemos un límite de compra cada 4 horas en los materiales de obra?** · 🟡 durante la beta

- *Por qué importa:* Sin límite, un grupo con oro compra todo, lo revende caro y frena la obra común.
- *Opciones:* Sí · No
- *Recomiendo:* Sí, en 10 a 15 materiales clave, con un tope generoso por persona.

**C-127. ¿Los oficios tienen un techo de nivel 40 durante la beta?** · 🟡 durante la beta

- *Por qué importa:* Están pensados para un año de juego. Programar ahora los rangos altos es trabajo que nadie va a ver pronto.
- *Opciones:* Sí, techo 40 · Todo completo
- *Recomiendo:* Sí, techo 40. Los rangos de arriba se programan antes de que alguien llegue.

**C-128. ¿Cuántos puestos de mercado tiene el Claro?** · 🟡 durante la beta

- *Por qué importa:* La escasez es a propósito (D-12). Si sobran no valen nada; si son muy pocos, quedan en manos de 3 o 4 gremios.
- *Opciones:* 10 · 25 · 50
- *Recomiendo:* Uno cada 20 jugadores activos, con máximo uno por jugador. Cada campamento nuevo suma los suyos.

**C-129. ¿La tasa autodeclarada (cualquiera puede comprarte el puesto al precio que declaraste) entra en la beta?** · 🟡 durante la beta

- *Por qué importa:* Es el corazón del mercado capitalista que pediste, pero un jugador rico puede comprar puestos ajenos uno tras otro.
- *Opciones:* Sí · Después
- *Recomiendo:* Sí, con un 2 % semanal sobre el valor declarado y 72 horas de protección después de cada compra.
- *Relacionada con:* P-53

### Ritmo y progresión (4)

**C-130. Con la curva de experiencia de la D-64, ¿cuántas horas de juego debería tomar llegar al nivel 10?** · 🟠 antes de la beta

- *Por qué importa:* La curva está fijada, pero cuánta experiencia da cada pelea y cada aporte no. Eso decide si la gente siente que avanza.
- *Opciones:* 2 a 3 horas · 6 a 8 horas · 15 a 20 horas
- *Recomiendo:* Unas 6 a 8 horas de juego activo, más o menos una semana jugando una hora por día.

**C-131. ¿Los primeros rangos útiles de los oficios llegan pronto?** · 🟡 durante la beta

- *Por qué importa:* En las primeras semanas hacen falta médicos y constructores con rango, o la salud y las obras se traban.
- *Opciones:* Sí · Curva lenta igual para todos
- *Recomiendo:* Sí: una curva calibrada para que Enfermero y Albañil lleguen en la primera semana del oficio y Médico en 3 a 4 semanas.

**C-132. ¿Cada cuánto se abre una región nueva con Guardián?** · 🟡 durante la beta

- *Por qué importa:* Cada región tiene que estar escrita y probada antes. Muy rápido agota el contenido; muy lento aburre.
- *Opciones:* Una por semana · Una cada 2 semanas
- *Recomiendo:* Como máximo una por semana, abierta por los jugadores al avanzar la Frontera. La siguiente siempre lista de antemano.

**C-133. ¿Cuánto dura una temporada, que es también el mandato del gobernador?** · 🟡 durante la beta

- *Por qué importa:* Unos documentos hablan de 3 a 4 meses y otros llaman temporada a las semanas de la fundación. Los mandatos y los rankings dependen de esto.
- *Opciones:* 1 mes · 3 meses · 4 meses
- *Recomiendo:* 3 meses. La primera empieza cuando se elige el primer gobernador.

### PvP, crimen y apuestas (5)

**C-134. ¿Cuándo se abre la primera zona con PvP libre?** · 🟡 durante la beta

- *Por qué importa:* Si abre en la primera semana, los que juegan más van a cazar a los recién llegados.
- *Opciones:* Semana 1 · Semana 3 · Después de la beta
- *Recomiendo:* No antes de la semana 3 de la beta, y sin saqueo hasta probar la Infamia.

**C-135. Sin pisos, ¿desde qué distancia al Claro se permite el PvP libre?** · 🟡 durante la beta

- *Por qué importa:* Las reglas de PvP, protección de novatos y saqueo dependían del número de piso. Con el mapa infinito hay que atarlas a la Lejanía, o no hay forma de decir dónde se está a salvo.
- *Opciones:* Desde Lejanía 8 · Más cerca · Nada de PvP en la beta
- *Recomiendo:* El Claro y las zonas cercanas (Lejanía 1 a 4), siempre sin PvP. El PvP libre, desde Lejanía 8.

**C-136. ¿Qué juegos de azar entran primero?** · 🟡 durante la beta

- *Por qué importa:* Cada formato suma riesgo legal y trabajo. Los más delicados son la lotería, los casinos de jugadores y el Foso.
- *Opciones:* Solo taberna · Todo lo diseñado · Nada de azar
- *Recomiendo:* Solo dados y cartas de taberna con oro, con tope diario y comisión. Lo demás, después.
- *Relacionada con:* P-41

**C-137. ¿Metemos una competencia simple entre gremios antes de la guerra de castillos?** · 🟡 durante la beta

- *Por qué importa:* Un público que pelea dos veces al día en TowerWars puede aburrirse antes de que haya castillos.
- *Opciones:* Sí, algo simple · No, esperar
- *Recomiendo:* Sí: una carrera semanal entre gremios por aportes a las obras, sin adelantar el cisma.

**C-138. ¿Se puede robar a otros jugadores dentro del Claro o de un campamento?** · 🟡 durante la beta

- *Por qué importa:* El crimen pone el carterismo en lugares concurridos, pero otras partes del diseño dicen que en zona segura no hay ataques entre jugadores.
- *Opciones:* Solo a PNJ · También a jugadores
- *Recomiendo:* No: en zona segura solo se roba a PNJ; a jugadores, solo en zonas peligrosas.

### Riesgos y seguridad (7)

**C-139. ¿Se permite una sola cuenta de Telegram por persona?** · 🟠 antes de la beta

- *Por qué importa:* Las cuentas falsas inflan votos, pasan oro y regalan energía con las invitaciones. La D-26 existe justo contra eso.
- *Opciones:* Una sola · Varias con límites
- *Recomiendo:* Sí, una por persona, escrito en las reglas. Las sospechosas se detectan por transferencias y horarios y se congelan hasta que alguien las revise.

**C-140. ¿La energía por invitar se paga cuando el invitado llega al nivel 5, en vez de apenas crea su héroe?** · 🟠 antes de la beta

- *Por qué importa:* Hoy basta con que el invitado cree su héroe (D-65). Cualquiera puede crear cuentas falsas en segundos y juntar hasta 40 de energía.
- *Opciones:* Al nivel 5 · Al crear el héroe, como hoy
- *Recomiendo:* Sí, al nivel 5 del invitado. El resto de la D-65 queda igual.

> En el juego hoy: el máximo de energía es 50 (D-78) y la extra por invitar puede llegar al doble, 100.

**C-141. Si alguien encuentra un error que duplica oro u objetos, ¿se premia a quien lo reporta y se castiga a quien lo explota?** · 🟠 antes de la beta

- *Por qué importa:* En toda beta aparece algún duplicado. Si reportar no paga, la gente se lo guarda. La regla tiene que estar publicada antes.
- *Opciones:* Sí · Solo castigo
- *Recomiendo:* Sí: quien reporta un error confirmado recibe el título 'Cazador de errores'. Quien lo explota pierde lo ganado y es suspendido; si repite, baneo.

**C-142. ¿A los bots y granjas de cuentas se les banea directo, sin la escalera de avisos?** · 🟠 antes de la beta

- *Por qué importa:* La escalera del diseño (aviso, congelar, suspensión, baneo) es lenta para los bots.
- *Opciones:* Baneo directo · Escalera normal
- *Recomiendo:* Baneo directo de todas las cuentas vinculadas, siempre después de una revisión humana.

**C-143. ¿El staff juega con una cuenta normal, separada de la que tiene poderes?** · 🟠 antes de la beta

- *Por qué importa:* Si un moderador compite con la misma cuenta con la que modera, cualquier victoria suya parece trampa.
- *Opciones:* Cuentas separadas · Misma cuenta con registro
- *Recomiendo:* Sí: una cuenta de jugador sin poderes y una cuenta de administración aparte, con registro de todo uso.

**C-144. ¿Aceptas que el juego se ponga solo en mantenimiento si detecta muchos errores o movimientos de oro raros?** · 🟠 antes de la beta

- *Por qué importa:* Un duplicado de madrugada puede durar horas antes de que alguien lo vea.
- *Opciones:* Sí · No
- *Recomiendo:* Sí, con aviso inmediato a ti y a un moderador. Además, un freno que congela solo el mercado si el oro creado en una hora se dispara.

**C-145. Si se descubre un duplicado de oro grave, ¿aceptas volver todo el servidor unas horas atrás?** · 🟠 antes de la beta

- *Por qué importa:* Volver atrás es lo más seguro para la economía, pero borra el progreso de quien jugó limpio, y la D-64 protege ese progreso.
- *Opciones:* Corrección puntual primero · Siempre volver atrás
- *Recomiendo:* Primero, una corrección puntual con los registros. Volver todo atrás solo con tu sí, si el abuso está muy repartido y se descubre en menos de 24 horas.

### Contradicciones del diseño (14)

**C-146. Hoy cualquiera aporta a la obra del Claro, pero la D-11 dice que construir es un oficio que se estudia: ¿cuál manda?** · 🟠 antes de la beta

- *Por qué importa:* El código y una decisión confirmada no coinciden. Si solo construyen los que estudiaron, el primer día casi nadie puede participar.
- *Opciones:* Todos aportan hasta la Aldea · Solo constructores ya
- *Recomiendo:* Cualquiera aporta materiales y hace trabajo simple hasta la Aldea. Desde ahí, las piezas importantes exigen rango de Construcción. Así se respeta la D-11 sin dejar a 500 mirando.

**C-147. ¿Cada etapa del Claro pide solo el rango de Construcción que se puede tener en ese momento?** · 🟠 antes de la beta

- *Por qué importa:* El diseño pide rangos altos para las obras grandes, y el primer día todos son principiantes. Sin ese ajuste, la fundación se traba.
- *Opciones:* Sí · Dejar los rangos del diseño
- *Recomiendo:* Sí: Campamento y Aldea con principiantes, Pueblo y Ciudad con Albañiles, y el primer Castillo con Oficiales de obra.

**C-148. Mientras no exista el Castillo, ¿quién enseña y examina los oficios?** · 🟠 antes de la beta

- *Por qué importa:* La D-11 pone entrenadores y exámenes en el Castillo, pero el mundo empieza sin Castillo.
- *Opciones:* PNJ del Claro · Esperar al Castillo
- *Recomiendo:* Los PNJ supervivientes del Claro enseñan y examinan los primeros rangos. El Castillo se queda con los rangos altos.

**C-149. ¿Congelamos lo que entra en el parche de beta, y las ideas nuevas van a una lista para después?** · 🟠 antes de la beta

- *Por qué importa:* La D-22 ('agregar todo lo posible') y la D-38 chocan con abrir pronto. Cada idea que entra antes de la beta la atrasa.
- *Opciones:* Sí, congelar · No, seguir sumando
- *Recomiendo:* Sí: el parche de beta queda cerrado. Lo nuevo se anota y entra en los parches siguientes.

**C-150. ¿Cambiamos los nombres visibles que son idénticos a la traducción oficial de WoW, como 'Golpe de Muerte'?** · 🟠 antes de la beta

- *Por qué importa:* Varios nombres de habilidades son la traducción oficial de WoW. Los IDs del código no se tocan, pero el nombre que ve el jugador sí, y cambiarlo es más barato antes de que 500 lo aprendan.
- *Opciones:* Renombrar ahora · Dejarlos
- *Recomiendo:* Sí: renombrar solo los textos visibles idénticos a WoW antes de la beta. Las mecánicas y los IDs quedan igual.
- *Relacionada con:* P-03

**C-151. ¿Las bandas de precio del mercado salen de una tabla fijada a mano durante el primer mes?** · 🟠 antes de la beta

- *Por qué importa:* La D-26 calcula las bandas con el historial de ventas, pero cuando abre el mercado no hay historial.
- *Opciones:* Sí, tabla inicial · Sin bandas al principio
- *Recomiendo:* Sí: precios de referencia con banda ancha (de la mitad al triple), que desde la tercera semana se recalcula sola.

**C-152. ¿Las cuentas nuevas no pueden regalar oro ni objetos durante sus primeras 72 horas?** · 🟠 antes de la beta

- *Por qué importa:* Es la regla contra las cuentas mula. Como el juego ya está en marcha, solo afecta a quien entra nuevo, no a todo el servidor.
- *Opciones:* Sí · Todo abierto
- *Recomiendo:* Sí: el mercado abierto desde el primer día, protegido por las bandas, y el regalo directo cerrado 72 horas para las cuentas nuevas.

**C-153. Mientras no haya médicos jugadores, ¿la sanadora PNJ del Claro trata heridas graves?** · 🟡 durante la beta

- *Por qué importa:* Las heridas graves piden un Médico o un sanatorio, y al principio no existe ninguno.
- *Opciones:* Sí, cara y lenta · No, solo jugadores
- *Recomiendo:* Sí, cara y lenta, como precio techo. Deja de atenderlas cuando haya 5 médicos jugadores activos.

**C-154. ¿Las clases sanadoras pueden curar enfermedades, o eso es solo trabajo de médicos?** · 🟡 durante la beta

- *Por qué importa:* El documento de balance dice que 4 clases curan enfermedades, el de curación dice que no, y la D-11 hace de curar un oficio que se estudia.
- *Opciones:* Solo médicos · Las clases también
- *Recomiendo:* Solo los médicos curan enfermedades. Las clases limpian solo efectos de combate (venenos y maldiciones de la pelea).

**C-155. ¿Karma e Infamia son la misma barra o dos distintas?** · 🟡 durante la beta

- *Por qué importa:* El PvP usa karma y el crimen usa Infamia. Hay que decidirlo antes de programar el PvP, porque los IDs del código no se cambian.
- *Opciones:* Una sola · Dos separadas
- *Recomiendo:* Una sola barra, la Infamia, que pinta el nombre de verde, naranja o rojo.
- *Relacionada con:* P-28

**C-156. La palabra 'Profundidades' nombra tres cosas distintas: ¿con cuál se queda?** · 🟡 durante la beta

- *Por qué importa:* Nombra la zona negra, el contenido en solitario con compañero y una dificultad. Los IDs del código no se cambian, así que hay que decidirlo antes de programar cualquiera de las tres.
- *Opciones:* Contenido en solitario · Zona negra · Dificultad
- *Recomiendo:* Profundidades es solo el contenido en solitario. La zona negra pasa a llamarse 'Tierras Negras' y la dificultad desaparece.

**C-157. Telegram no dice de qué país es cada jugador: ¿se lo preguntamos?** · 🟡 durante la beta

- *Por qué importa:* El diseño promete apagar las apuestas en una región si una ley lo pide, y sin el país no se puede.
- *Opciones:* Sí, preguntar · No
- *Recomiendo:* Sí, la primera vez que entra a las apuestas: una pregunta de un toque, con la opción 'prefiero no decir'.

**C-158. ¿La primera subasta de puestos de mercado se hace al llegar a Pueblo, antes de lo que dice el diseño?** · 🟡 durante la beta

- *Por qué importa:* El diseño abre las subastas en la Ciudad, pero las pujas son parte central de la economía (D-12). En la Aldea todavía nadie tiene oro.
- *Opciones:* Desde la Aldea · Desde el Pueblo · Desde la Ciudad
- *Recomiendo:* Sí: en la Aldea abre el mercado de órdenes sin puestos, y la primera subasta de puestos llega con el Pueblo.

**C-159. ¿Usamos una sola escala de dificultad para mazmorras, Profundidades y bandas?** · ⚪ después

- *Por qué importa:* Hoy hay tres escalas distintas, y 'Pesadilla' también es el nombre de un contenido de cordura.
- *Opciones:* Sí, una sola · Dejarlas
- *Recomiendo:* Sí: Normal, Heroica, Mítica y Mítica+ para todo lo instanciado; 'Pesadilla' solo para el contenido de cordura.
