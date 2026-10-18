# Informes del juego en el chat del equipo

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Arquitectura modular](arquitectura-modular.md) (M20 Administración y telemetría), [Telegram](telegram.md) · **Alimenta a:** el balance (los números que se miden en vez de fijarse a dedo, D-238.1), la [hoja de ruta](../00-vision/hoja-de-ruta.md) fase 1 · **Estado:** confirmado por el dueño (D-260, 17-oct-2026) y en el juego desde la 0.33

El dueño pidió (17-oct-2026) un chat para los informes: "ahí vamos a empezar a mandar todos los reportes en archivos directamente. El primer reporte van a ser los reportes de los jugadores: qué van haciendo, las analíticas de cuánto farmean, cómo lo hacen y todo lo demás… no por jugador, sino genérico; coge a 10 jugadores de acuerdo a la actividad". Es la primera pieza de la telemetría con exportación diaria de D-241.4.

---

## 1. Qué llega al chat

| Qué | Cuándo | Cómo |
|---|---|---|
| 📊 **Informe de jugadores** | Una vez por día: la primera vez que el bot mira en el día (UTC) y, si Telegram lo rechaza, de nuevo a la hora | Un archivo `informe-jugadores-AAAA-MM-DD.txt` |
| 💬 **Feedback** de un jugador (D-258) | Apenas lo escribe | Un mensaje con el héroe, su nivel, su idioma y el texto |

El chat sale de la variable `RPG_REPORTS_CHAT_ID`. Si no está, se usa el chat que dio el dueño. El número del chat no es una credencial: sin el token del bot no sirve para nada.

**El número del chat (0.33.1, D-263).** Un grupo común tiene un número como `-4365890113`; un supergrupo lleva `-100` delante (`-1004365890113`). Si Telegram dice "chat no encontrado", el bot prueba la otra forma; si el grupo pasó a supergrupo, sigue al número nuevo. Recuerda el que funcionó y lo anota en el registro ("reports chat: …"). Cuando agregan al bot a un chat, el registro anota su número real ("bot membership: chat …") y el informe que esperaba se intenta enseguida. El bot nunca manda informes a otro grupo, aunque lo agreguen ahí. En los grupos el bot no juega (D-262, [Telegram](telegram.md) §6).

## 2. Qué trae el informe de jugadores

Es **genérico**: sin nombres ni cuentas. Mira a todos los que jugaron en la última semana y toma como muestra a los **10 más activos**: los que más experiencia sumaron desde el informe anterior (el primer día, los que jugaron más reciente).

1. **Cuántos:** héroes creados, cuántos jugaron en 24 horas y en 7 días.
2. **Quiénes son:** nivel (promedio, mínimo y máximo), clases, idiomas y si tienen campamento.
3. **Qué hacen ahora:** viajando, explorando, recolectando, cazando, descansando, peleando o sin hacer nada.
4. **Cuánto juegan y juntan, por día y en total:**
   - unidades recolectadas;
   - carne y piel del 🔪 Desollador;
   - puntos de 🧭 Explorador;
   - peleas ganadas;
   - experiencia de refinar y fabricar, y de 💱 Comercio;
   - experiencia de héroe, zonas descubiertas y monedas;
   - y en qué reparten el tiempo (recolectar, explorar, pelear o fabricar).
5. **Oficios:** cuáles aprendieron (D-257) y el rango promedio de los que suben solos.
6. **Mochila y economía:** monedas por jugador y lo que más llevan.
7. **Mapa:** a cuántas zonas de la fogata andan y cuántas recuerdan.
8. **Feedback:** cuántos mensajes llegaron en 24 horas.

**Cómo compara un día con otro.** Cada informe guarda una foto de los números de cada héroe (espacio `report_snap`, clave el día) y el siguiente informe resta. El primer informe con foto solo trae totales y lo dice.

## 3. Reglas

1. **Solo lee el juego.** Nunca cambia un héroe, un campamento ni una regla. Lo único que escribe es su foto del día y la marca del último informe (espacio `reports`).
2. **Sin nombres.** El informe es de todos juntos. El feedback sí lleva el nombre del héroe: el jugador lo ve antes de escribir.
3. **Para el equipo, en español.** No pasa por los archivos de idiomas porque no lo ve ningún jugador.
4. **Un error nunca para al bot:** si Telegram rechaza el archivo (por ejemplo, el bot no está en el chat), se anota en el registro y se intenta a la hora. El 💬 Feedback que no pudo salir vuelve a la cola y sale en el próximo intento: ninguno se pierde (0.33.1).

## 4. Cómo está hecho

| Pieza | Dónde |
|---|---|
| El informe | `adapters/reports.py` (`build`, `due`, `mark_sent`) |
| El envío | `adapters/telegram/bot.py` (`send_reports`, dentro de `notifier`, cada 15 segundos) |
| El feedback | `engine/service/game.py` (`_feedback_view`, `_save_feedback`, `take_feedback`, `return_feedback`; espacio `feedback`) |
| El número del chat | `adapters/telegram/bot.py` (`report_chats`, `post_to_reports`) |
| Pruebas | `tests/test_fogata_ordenada.py` y `tests/test_solo_privado.py` |

## 5. Lo que puede venir después

- Más informes en el mismo chat: economía (monedas que entran y salen), combate (dónde mueren los héroes), oficios (qué se fabrica). La hoja de ruta los pone en la fase 1, "medir antes de tocar".
- Registrar cada acción (D-241.4) para informes más finos. Hoy el informe sale de los números que ya guarda cada héroe.

## De dónde sale

- **El pedido es del dueño** (17-oct-2026).
- **Mandar los informes a un chat de Telegram** es lo habitual en los bots de juego: el equipo los lee en el mismo lugar donde habla.
- **Comparar fotos diarias** en vez de registrar cada acción es la forma liviana de las analíticas de juegos chicos: alcanza para ver cuánto juega la gente y en qué, sin cargar la base de datos.
