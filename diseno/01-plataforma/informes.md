# Informes del juego en el chat del equipo

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Arquitectura modular](arquitectura-modular.md) (M20 Administración y telemetría), [Telegram](telegram.md) · **Alimenta a:** el balance (los números que se miden en vez de fijarse a dedo, D-238.1), la [hoja de ruta](../00-vision/hoja-de-ruta.md) fase 1 · **Estado:** confirmado por el dueño (D-260, 17-oct-2026; D-341, 24-oct-2026) y en el juego; cómo se aplicó el informe por jugador: D-344, provisional

El dueño pidió (17-oct-2026) un chat para los informes: "ahí vamos a empezar a mandar todos los reportes en archivos directamente. El primer reporte van a ser los reportes de los jugadores: qué van haciendo, las analíticas de cuánto farmean, cómo lo hacen y todo lo demás… no por jugador, sino genérico; coge a 10 jugadores de acuerdo a la actividad". Es la primera pieza de la telemetría con exportación de D-241.4.

El 24-oct-2026 lo cambió (D-341): "cuando estemos dando los informes diarios, quiero que me saque los promedios de jugadores activos con más detalles, quiénes son, con su arroba. Y cuál es el tipo de contenido que más hacen. O sea, la especificación de cuánto juegan y juntan, eso lo quiero por jugador. Aunque sea largo el documento, no importa. Pero que sea más detallado. Incluso pueden ser varios documentos al día, no pasa nada." Y: "La idea es que los documentos que vayan llegando a Lost Realms Report sean como un reporte constante de base de datos. Para evitar que el servidor se sobrecargue." Sus respuestas: **cada 3 horas**; **un .txt para leer y un .csv** con una fila por jugador; **el servidor guarda solo 3 días** ("el servidor solo el último reporte de jugador y general de los últimos 3 días no más, el resto al grupo de reportes"); y van **todos los que jugaron en las últimas 24 horas**, con su tarjeta, del más activo al menos, y al final quién dejó de venir.

---

## 1. Qué llega al chat

| Qué | Cuándo | Cómo |
|---|---|---|
| 📊 **Informe de jugadores** (D-341) | Cada 3 horas: a las 00, 03, 06, 09, 12, 15, 18 y 21 (UTC). Si el bot estuvo apagado varios tramos, llega **uno solo** que cubre desde el último que salió | Dos archivos: `informe-jugadores-AAAA-MM-DD-HHh.txt` (para leer) y `datos-jugadores-AAAA-MM-DD-HHh.csv` (una fila por jugador; se abre en Excel o Google Sheets), con el texto "📊 Informe de jugadores · AAAA-MM-DD HH:MM UTC" |
| 💬 **Feedback** de un jugador (D-258, D-275) | Apenas lo escribe | Una tarjeta con su @, tipo, prioridad, paso y botones (§1.1) |

El chat sale de la variable `RPG_REPORTS_CHAT_ID`. Si no está, se usa el chat que dio el dueño. El número del chat no es una credencial: sin el token del bot no sirve para nada.

**El número del chat (0.33.1, D-263).** Un grupo común tiene un número como `-1234567890`; un supergrupo lleva `-100` delante (`-1001234567890`). Si Telegram dice "chat no encontrado", el bot prueba la otra forma; si el grupo pasó a supergrupo, sigue al número nuevo. Recuerda el que funcionó y lo anota en el registro ("reports chat: …"). Cuando agregan al bot a un chat, el registro anota su número real ("bot membership: chat …") y el informe que esperaba se intenta enseguida. El bot nunca manda informes a otro grupo, aunque lo agreguen ahí. En los grupos el bot no juega (D-262, [Telegram](telegram.md) §6).

### 1.1 El 💬 Feedback, con su tipo, su prioridad y sus pasos (D-275, desde la 0.35)

El dueño pidió (18-oct) que el feedback llegue "con el arroba, una descripción clasificada de acuerdo al tipo de problema y las notas del jugador para darle prioridad", con "botones de acción… hasta cerrar el feedback como resuelto".

- **El jugador elige el tipo** al tocar 💬 Feedback: 🐞 Error, 💡 Idea, ⚖️ Balance, ❓ No se entiende u 💬 Otro (`feedback.kinds`), y después escribe. Si escribe directo, el tipo sale de sus palabras (`feedback.keywords` en los archivos de idiomas, en cualquier idioma).
- **La tarjeta del chat** (`adapters/feedback_desk.py`) trae el tipo, la prioridad, el paso y su número (#fb12); el @ del jugador (o un enlace a su chat si no tiene @); su héroe, clase, nivel e idioma; dónde estaba; la versión del juego; su texto; y el historial de quién tocó cada botón y cuándo (hora UTC).
- **Prioridad:** arranca según el tipo (`feedback.kind_priority`: error 🔴, balance y "no se entiende" 🟡, idea y otro 🟢) y el equipo la cambia con 🔴 🟡 🟢.
- **Pasos:** 🆕 Nuevo → 👀 Visto → ✅ Aprobado → 🔧 En arreglo → ✔️ Resuelto, con ❌ Descartar en cualquier paso; cerrado, ↩️ Reabrir vuelve a 👀 Visto. Cada botón edita la tarjeta. Los botones solo valen en el chat de informes.
- **Al resolverse**, al jugador le llega "✔️ Tu mensaje sobre «…» quedó resuelto. ¡Gracias!" en su idioma. Si se descarta, no se le avisa.
- Cada feedback se guarda con un número propio (espacio `feedback`, clave el número; el contador en `meta`/`feedback_seq`).

## 2. Qué trae el informe de jugadores (D-341, D-344)

Cada informe mira dos ventanas: **la ventana** (las últimas 3 horas hasta el comienzo del tramo; después de un apagón, desde el último informe que salió) y **las últimas 24 horas**. Lo de la hora que se está jugando sale en el informe siguiente.

**El .txt, sección por sección:**

1. **Cuántos:** héroes en total y nuevos (en la ventana y en 24 h); jugadores activos en la ventana, en 24 h y en 7 días; cuántos tuvieron lotes que siguieron solos sin tocar botones; cuentas sin héroe que tocaron botones.
2. **Promedios por jugador activo** (ventana y 24 h, entre los que tienen botones medidos): botones, minutos activos, sesiones, minutos de actividades con tiempo, unidades recolectadas, peleas (ganadas y perdidas), fabricaciones, experiencia y monedas que entraron y salieron.
3. **Qué hacen más:** el reparto de los botones por tipo de contenido (§2.1) y del tiempo por actividad (viajar, explorar, recolectar, talar, pescar, cazar, descansar), en la ventana y en 24 h; y cuántos jugadores tienen cada tipo como su **contenido principal**.
4. **Lo que más se recolecta** (ventana y 24 h), objeto por objeto, y los hallazgos al explorar.
5. **Quiénes son** (los de las tarjetas): nivel, clases, roles, idiomas, campamento o gremio.
6. **Oficios:** cuáles aprendieron y cuántos rangos de oficio subieron en 24 h.
7. **Mochila y economía:** monedas, tipos usados de la mochila (de 50, desde la 0.62) y lo que más llevan.
8. **Mapa:** a cuántas zonas del Claro andan, cuántas recuerdan y a cuántas llegaron viajando.
9. **Feedback:** cuántos mensajes llegaron en 24 horas.
10. **Mercado entre jugadores** (0.46, D-320): de ayer y de hoy hasta ahora, cuántas compras hubo, cuántas unidades y monedas cambiaron de mano, cuánto impuesto se quemó y cuántas órdenes se publicaron, cancelaron o vencieron; y cuántas órdenes hay abiertas. Desde la 0.59 (D-335), lo mismo de los 📜 pedidos de fabricación. Sale de lo que el 🏛️ Mercado y los pedidos anotan cada día en `market_log` (`market_lines`).
11. **Dejaron de venir:** quién jugó en los últimos 7 días pero no en las últimas 24 horas, con su @, su héroe, su nivel y cuándo jugó por última vez.
12. **Malla convertida en cuero** (solo si existe `migrations`/`malla_to_leather`, la conversión de la 0.62.2, y solo en los informes de los 3 días que siguen al cambio, lo mismo que guarda el servidor): a quién se le convirtió qué, con su @; si nadie tenía malla, una línea lo dice ("Nadie tenía piezas de malla").
13. **Una tarjeta por jugador** (sección 12 si no hay la de la malla) activo en las últimas 24 horas, del más activo al menos (por botones, minutos activos, tiempo de actividades y lo recolectado): su @ (o "sin @"), héroe y cuenta; clase, rol, nivel (y niveles ganados) e idioma; campamento o gremio; dónde está, qué hace ahora y su último botón; minutos activos y sesiones (ventana y 24 h); el tiempo de cada actividad; los botones por tipo con su porcentaje y **lo que más hace** (por botones y por tiempo); lo que recolectó objeto por objeto; los hallazgos; vueltas de explorar y recolectar y zonas a las que llegó; peleas ganadas, perdidas y huidas; lo que fabricó; experiencia y rangos de oficio; monedas que entraron y salieron y las que tiene; el 🏛️ Mercado y el 🛒 mercader; mazmorras, misiones, encargos y aportes al campamento; el rango de cada oficio; la mochila (tipos usados, equipo suelto, mochilas de oficio puestas) y las piezas de equipo puestas.

**El .csv:** una fila por jugador de las tarjetas, con los mismos números en columnas de 3 horas y de 24 horas (también los botones de cada tipo), y una fila de títulos. Va en UTF-8 con la marca BOM, así Excel muestra bien las tildes; los valores van separados por coma (E-291 pregunta si en el Excel del dueño se abre en columnas).

### 2.1 Qué se mide y cómo (D-344, provisional)

- **Un botón o un texto** que manda el jugador cuenta **una vez** (si un texto abre un botón por dentro, cuenta uno solo), con su **tipo de contenido**: explorar; recolectar (también talar y pescar); cazar y pelear (un botón que cae en una pelea, como una poción, es pelear); viajar y mapa; fabricar, refinar, cocinar y oficios (también encantar, reparar, especializaciones, títulos y libros); mercado y mercader (también los 📜 pedidos y los 💎); campamento y gremio (obras, depósitos, fondo, escuadras, armería, invitaciones); mazmorras; misiones y tablón (también el 🧭 camino guiado); social y chat (el chat del gremio, los gestos, 👥 Jugadores); héroe, equipo y mochila; y menús y otros (📍 Zona, ⚙️ Opciones, ❓ Dudas, 💬 Feedback, la creación del héroe). Un botón nuevo que no está en la lista cuenta como "menús y otros" hasta sumarlo.
- **Contenido principal:** el tipo con más botones, sin contar "menús y otros" ni "héroe, equipo y mochila" si hay otro.
- **Minutos activos:** los minutos distintos en los que tocó al menos un botón. **Sesiones:** una pausa de más de 15 minutos corta la sesión.
- **Minutos de actividades con tiempo:** el tiempo de los viajes, los lotes de explorar, recolectar, talar, pescar y cazar, y el descanso que el héroe empezó, contado a medida que cada vuelta o cada tramo arranca (si se corta antes, cuenta lo que ya había empezado).
- **Unidades recolectadas:** las que **entran de verdad** a la mochila al recolectar, talar y pescar (con la unidad de más del oficio, el nodo y los raros) y al despellejar (carne y piel). No salen de la experiencia de oficio, que desde la 0.33 no sube si el oficio no está aprendido. Los hallazgos al explorar van aparte.
- **Experiencia, niveles y monedas:** la diferencia entre un guardado del héroe y el siguiente (las monedas que entran y las que salen, por separado).
- **Activo:** tocó al menos un botón en la ventana (o su último botón cae en ella). Quien solo tuvo un lote que siguió solo también tiene tarjeta, al final.
- **Desde cuándo:** el informe dice desde qué hora hay medición por jugador; lo de antes solo se ve en las fichas (nivel, monedas, último botón).

## 3. Reglas

1. **Solo lee el juego.** Nunca cambia un héroe, un campamento ni una regla. Medir nunca corta una jugada: si algo falla al contar, el juego sigue y el informe dice cuántas veces falló.
2. **Con nombres y @, solo para el equipo** (D-341, reemplaza la regla "sin nombres" de D-260). El informe va solo al chat de informes; nunca a un jugador ni a otro grupo. El feedback también lleva el nombre del héroe: el jugador lo ve antes de escribir.
3. **Para el equipo, en español.** No pasa por los archivos de idiomas porque no lo ve ningún jugador.
4. **Liviano para el servidor** (D-341: "para evitar que el servidor se sobrecargue"). Nada se escribe por botón: los contadores viven en la memoria y se guardan como mucho una vez por minuto, uno por jugador y por tramo de 3 horas. Si el bot se reinicia, se pierde como mucho el último minuto.
5. **El servidor guarda 3 días** (D-341). Los contadores, los informes armados y lo viejo del informe diario se borran a los 3 días; la historia completa queda en el chat. Nunca se borra el progreso de nadie ni lo de otros módulos (por ejemplo, `market_log` es del mercado).
6. **Sin avalancha:** uno por tramo. Si el bot estuvo apagado, sale uno solo que cubre desde el último que salió (como mucho 3 días). Si Telegram rechaza los archivos, el mismo informe se intenta a la hora (o apenas agregan al bot a un chat), sin repetir el archivo que ya salió; si mientras tanto termina otro tramo, el nuevo reemplaza al que no salió y cubre los dos.
7. **Un error nunca para al bot:** si Telegram rechaza el archivo, se anota en el registro. El 💬 Feedback que no pudo salir vuelve a la cola y sale en el próximo intento: ninguno se pierde (0.33.1).

## 4. Cómo está hecho

| Pieza | Dónde |
|---|---|
| La medición | `engine/service/telemetry.py` (`TelemetryMixin`, de la que hereda `GameService`): `tracked` en `act()` y `text()`; `_tel_saved` en `_save`; `_tel_tick` en `tick()`; escucha `HeroCreated`, `ItemCrafted`, `CombatEnded`, `ProfessionRankUp`, `TravelArrived`, `BossDefeated` y `HeroFellForever`; ganchos en `_story_event` (`_tel_story`), `_end_combat` (lo despellejado), `_explore_step` (el hallazgo), `_buy`, `_dng_fight`, `_quest_complete`, `_claim_daily`, `_market_buy` y `_market_fill`. Espacio `telemetry` (clave "<tramo>:<cuenta>") |
| El informe | `adapters/reports.py` (`due`, `generate`, `pending`, `mark_sent`, `build`, `prune`, `market_lines`, `malla_lines`). Espacios `reports` (clave `slots`) y `report_out` (los informes armados, 3 días) |
| El envío | `adapters/telegram/bot.py` (`send_reports`, dentro de `notifier`, cada 15 segundos) |
| El @ del jugador | `GameService.set_handle` (lo guarda el bot en `prefs`, D-275) |
| El feedback | `engine/service/game.py` (`_feedback_view`, `_feedback_classify`, `_save_feedback`, `set_handle`, `take_feedback`, `return_feedback`, `feedback_update`; espacio `feedback`) y `adapters/feedback_desk.py` (la tarjeta y sus botones) |
| El número del chat | `adapters/telegram/bot.py` (`report_chats`, `post_to_reports`) |
| Pruebas | `tests/test_informes_por_jugador.py` (el informe y la medición), `tests/test_fogata_ordenada.py`, `tests/test_solo_privado.py`, `tests/test_feedback_equipo.py` y `tests/test_mercado.py` |

## 5. Lo que puede venir después

- Más informes en el mismo chat: economía (monedas que entran y salen por fuente y sumidero), combate (dónde mueren los héroes), oficios (qué se fabrica). La hoja de ruta los pone en la fase 1, "medir antes de tocar".
- El balance de cada número con lo medido (D-238.1): cuánto se recolecta por hora de lote, cuánto tarda cada camino en subir.
- Si hay muchos jugadores, el informe puede partirse en varios archivos (el dueño dijo que pueden ser varios al día).

## De dónde sale

- **El pedido es del dueño** (17-oct-2026 y 24-oct-2026).
- **Mandar los informes a un chat de Telegram** es lo habitual en los bots de juego: el equipo los lee en el mismo lugar donde habla.
- **Contar en memoria y guardar de a ratos** es como guardan las analíticas los juegos que no quieren cargar la base de datos: se agrupa por jugador y por tramo, y se escribe una vez por minuto en lugar de una vez por acción.
- **Sesiones cortadas por una pausa** (aquí, 15 minutos) es la medida de las analíticas de juegos y aplicaciones para saber cuántas veces vuelve alguien en el día.
