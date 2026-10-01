# Telegram como plataforma

> **Módulo** [01 · Plataforma](README.md) · **Condiciona a:** todos los módulos · **Estado:** propuesta

> **Nota: Telegram es el primer cliente, pero no el único** (D-40, D-41). Todo lo que este documento describe con funciones de Telegram (dados nativos, reenvíos, encuestas, grupos y temas, modo inline, Mini Apps, Stars, límites de largo y de botones, mensajes vivos) tiene su regla neutral y su equivalente web en [Web y multiplataforma](web-y-multiplataforma.md). Los ejemplos "Cómo se ve en Telegram" de todo el diseño son una representación entre varias.

Antes de diseñar un solo sistema hay que aceptar dónde vive el juego. Telegram no es una pantalla de juego: es un chat. Todo el diseño está pensado para funcionar **con mensajes, botones y turnos**, nunca en tiempo real.

---

## 0. El bot

- El juego se monta en **[@thetowerwarbot](https://t.me/thetowerwarbot)**.
- Es un bot **distinto** de **@TowerWarsBot** (TowerWars), que sigue su camino y no se toca.
- El token del bot va en una variable de entorno del servidor (por ejemplo `TELEGRAM_BOT_TOKEN`), **nunca** en el repositorio.
- No se despliega nada, en Railway ni en ningún otro lado, hasta que el dueño lo diga.

Ver decisiones D-01 a D-03 en [Decisiones](../00-vision/decisiones.md).

## 1. Lo que Telegram nos da

| Función | Qué permite | Quién ya la usa | Para qué la usamos |
|---|---|---|---|
| Teclados inline + edición de mensajes | Un solo mensaje que se actualiza en lugar de mandar cien | UNO, Chessy, Chat Wars | Combate, mapa, crafteo: **un mensaje vivo por actividad** |
| Menú persistente (reply keyboard) | Botonera fija abajo | Chat Wars, TowerWars | Navegación principal |
| Modo inline | Información privada dentro de un grupo | UNO (tu mano solo la ves tú) | Cartas de taberna, fichas, inventario sin spam |
| Plataforma de juegos HTML5 | Minijuego con récord por chat (`setGameScore`) | @gamebot, GAMEE | Minijuegos de destreza (forja, pesca, ganzúa) |
| Mini Apps (WebApp) | Pantalla web completa dentro de Telegram | Hamster Kombat, Catizen, Not Pixel | Solo lo que el texto no aguanta: mapa, árbol de talentos, gráfico del mercado |
| Dados animados nativos 🎲🎯🏀⚽🎳🎰 | Valor aleatorio decidido **por el servidor de Telegram**, visible para todos | Bots de apuestas y de rol | Tiradas de botín, dados de taberna, "Necesidad/Codicia" a la vista |
| Telegram Stars | Pagos digitales compatibles con Apple y Google | Catizen y casi todas las Mini Apps | Monetización (ver [Monetización](../07-economia/monetizacion.md)) |
| Encuestas en modo quiz | Preguntas con respuesta correcta, tiempo y ranking | @QuizBot oficial | Trivia de lore, votaciones de gremio |
| Spoilers y citas plegables | Ocultar o plegar texto largo | Varios | Registro de combate plegado: resumen visible, detalle al tocar |
| Reenvío con cabecera "reenviado de @bot" | La cabecera funciona casi como una firma | Chat Wars (informes), TowerWars (vales del gremio) | Pruebas de hazañas, contratos, vales, informes de batalla |
| Temas (topics) en grupos | Canales internos dentro de un grupo | Comunidades grandes | Chat de gremio con #órdenes, #banda, #mercado, #taberna |
| Canales | Difusión de una vía | Chat Wars (partes de batalla) | Gaceta de la Torre, precios, Salón de los Caídos |

## 2. Lo que Telegram nos prohíbe

| Límite | Valor | Consecuencia de diseño |
|---|---|---|
| Largo de mensaje | 4.096 caracteres (pie de foto: 1.024) | Pasarse no corta: **no sale nada**. Todo mensaje largo se pagina o se pliega (lección de TowerWars) |
| `callback_data` | 1 a 64 bytes | Los botones mandan identificadores cortos; el estado vive en el servidor |
| Envíos por chat | ~1 mensaje por segundo | Una banda de 20 no puede recibir un mensaje por golpe |
| Envíos por grupo | ~20 mensajes por minuto | En grupo se edita un resumen cada 3-5 s; nunca un mensaje por evento |
| Envíos globales | ~30 por segundo (difusión de pago hasta 1.000/s con Stars) | Los avisos masivos se escalonan |
| Mensaje privado | El bot no puede escribirte si no le diste `/start` | Toda invitación a actividad de grupo pasa primero por el privado |
| Modo privacidad en grupos | El bot solo ve comandos, salvo que sea administrador | Lo que depende de la conversación del grupo exige que el bot sea admin |
| Pantallas chicas | Un botón largo se trunca | **El costo nunca va en el botón** (lección de TowerWars). Máximo 2-3 botones por fila |

Telegram no documenta oficialmente las cifras de envío y pueden cambiar; se diseña con margen.

## 3. Diez principios que salen de lo anterior

1. **Un mensaje vivo por actividad.** Combate, crafteo y exploración editan su propio mensaje. Solo se manda uno nuevo cuando algo pide atención: te toca, te atacan, terminó.
2. **Rondas, nunca reflejos.** Nada depende de la velocidad del pulgar. En grupo, rondas simultáneas con temporizador (45-90 s); en solitario, sin temporizador. TowerWars ya probó rondas de 90 s en su Torre de Gremio y funcionan.
3. **Tres ritmos de sesión.** Todo sistema declara a cuál pertenece:
   - **Toque** (1-3 minutos): cobrar, encolar encargos, revisar el mercado, curarse.
   - **Sesión** (15-45 minutos): mazmorra, crafteo manual, expedición, arena.
   - **Cita** (a hora fija): guerra de facciones, bandas, asaltos a Guardianes, torneos.
4. **Resumen arriba, detalle plegado.** Cinco líneas cuentan qué pasó; quien quiera cada número abre la cita plegable o pide el parte en `.txt`.
5. **Lo privado va al privado.** Mano de cartas, rol secreto, inventario: por mensaje directo o modo inline, nunca en el grupo.
6. **Ocho botones de combate como máximo.** Más no cabe ni se lee (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)).
7. **El azar importante se ve.** Si una tirada decide quién se lleva el botín, se tira con el dado nativo en el chat del grupo.
8. **El reenvío es una firma.** Un informe reenviado prueba una hazaña; un vale reenviado mueve objetos.
9. **Mini App solo donde el texto no alcanza.** El juego completo tiene que poder jugarse sin abrirla.
10. **Nada que se gane pulsando lo mismo.** Es lo que atrae bots y granjas de multicuentas (ver [Seguridad](seguridad-y-anti-trampas.md)). Lo repetitivo se automatiza de forma oficial (cola de encargos, [Tácticas](../04-combate/avisos-y-tacticas.md)) para que un bot pirata no tenga nada que ganar.

## 4. Dónde ocurre cada cosa

| Lugar | Qué pasa ahí |
|---|---|
| **Privado con el bot** | Todo lo personal: héroe, inventario, cuerpo, crafteo, encargos, combate en solitario, mazmorras (en salas retransmitidas) |
| **Grupo de facción** | Órdenes de guerra, anuncios, reclutamiento |
| **Grupo del gremio** (con temas) | #órdenes (mensaje fijado), #banda, #mercado, #taberna, #rol |
| **Grupos públicos por piso** | Chat de zona: comercio local, apariciones de criaturas y reliquias, jefes errantes |
| **Canal Gaceta de la Torre** | Primeras muertes de jefes, avance del Frente, caídas del Juramento de Hierro, partes de guerra |
| **Canal del Mercado** | Precios de referencia por ciudad, órdenes grandes, informe económico mensual |
| **Mini App** (fase tardía) | Mapa del piso, árbol de talentos, libro de órdenes con gráfico, vivienda |

**Salas retransmitidas.** Un bot no puede crear grupos. Por eso el contenido armado al azar (mazmorra por buscador) ocurre en privado: el bot envía a cada participante el mismo mensaje vivo y le reenvía el chat de los demás. TowerWars ya lo hace en su Torre de Gremio; aquí es el mecanismo de todo el contenido de grupo.

## 5. Carga del servidor

- Los eventos de combate se agrupan y se aplican **una vez por ronda**, no por acción.
- Las ediciones se limitan a una cada 3-5 s por chat, con cola.
- Los avisos masivos (evento de servidor, apertura de piso) se escalonan en minutos y se anuncian primero en el canal.
- Todo temporizador vive en el servidor con cálculo perezoso: si el bot se reinicia, nada se pierde.
