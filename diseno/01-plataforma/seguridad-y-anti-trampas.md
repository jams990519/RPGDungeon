# Seguridad y anti-trampas

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Economía](../07-economia/economia.md), [PvP](../06-contenido/pvp.md) · **Estado:** propuesta

Un juego de Telegram es fácil de automatizar y fácil de multiplicar: crear una cuenta cuesta un número de teléfono. Los juegos longevos de la plataforma lo sufrieron. Chat Wars tuvo *userbots* que jugaban solos (gastaban estamina, iban a la arena, seguían órdenes de guerra). TapSwap retrasó su lanzamiento por granjas de bots. Hamster Kombat baneó 2,3 millones de cuentas por trampas (ver [investigación](../99-referencias/investigacion-juegos-telegram.md)).

---

## 1. Principio: que no haya nada que ganar con un bot

La defensa más barata es el diseño:
- **Nada se gana pulsando lo mismo.** No hay "toca 1.000 veces".
- **Lo repetitivo está automatizado oficialmente**: la cola de encargos y las [Tácticas](../04-combate/avisos-y-tacticas.md) hacen lo que haría un bot. Un bot pirata no da ventaja.
- **La recompensa grande pide decisiones**: leer avisos de jefes, elegir rutas, negociar, fabricar.
- **Topes diarios y semanales** en lo que más se abusaría (Enfoque de fabricación, recompensas de mazmorra, PvP con la misma persona).

## 2. Multicuentas

| Riesgo | Medida |
|---|---|
| Cuentas "mula" que regalan todo a la principal | Las cuentas nuevas no pueden transferir oro ni objetos durante sus primeros días, ni por encima de un tope hasta cierto nivel |
| Inflar votos, invasiones o guerras con cuentas vacías | Solo cuentan en la guerra de facciones los jugadores activos en los últimos 3 días (regla probada en TowerWars) y con nivel mínimo |
| Granjear recompensas de invitación | Las invitaciones pagan cuando el invitado llega a cierto nivel, no al registrarse |
| Una persona en varias facciones | Se permite (cada cuenta es un jugador), pero una persona no puede tener dos cuentas en guerras enfrentadas en la misma batalla si se detecta el vínculo |

**Detección:** patrones de transferencias, horarios idénticos, rutas idénticas, el mismo dispositivo en la Mini App. Todo pasa por el módulo de anti-trampas (M23) y termina en una revisión humana antes de sancionar.

## 3. Bots y macros

- **Retos contextuales** en momentos sensibles, en lugar de captchas genéricos: "¿Cuántas heridas tiene tu brazo izquierdo?", "¿Qué dijo el aviso del jefe en la ronda anterior?". Un humano responde en un segundo; un script, no.
- **Ritmo humano**: acciones con una regularidad imposible (cada 30,0 s durante 10 horas) se marcan.
- **API oficial de solo lectura** para herramientas legítimas de la comunidad (calculadoras, rastreadores de precios). Chat Wars tuvo una y redujo la necesidad de bots piratas.

## 4. Comercio con dinero real

- Prohibido y detectado: transferencias muy desbalanceadas (1 cobre por una espada épica), cuentas que solo reciben, precios anómalos.
- La mejor defensa es que el oro tenga un canal legal si se decide monetizar así (ver [Monetización](../07-economia/monetizacion.md)).
- Impuestos y un porcentaje quemado en las transferencias entre jugadores frenan el lavado de oro (el bot Iris quema un 5 % de cada transferencia de su moneda).

## 5. Sanciones

Escalonadas y públicas en su criterio, no en su nombre: aviso → congelación de comercio → suspensión temporal → baneo. Nada automático sin revisión humana, salvo el congelamiento preventivo.

## 6. Datos y privacidad

- Se guarda lo mínimo: ID de Telegram, idioma, datos del juego.
- Los números de teléfono nunca llegan al bot (Telegram no los da si no se piden).
- **Credenciales: nombres de variables de entorno sí, valores jamás** en el repositorio (regla heredada de TowerWars).

## 7. Moderación de chats

Los grupos oficiales (facción, pisos, taberna) necesitan moderación: filtro de palabras, límite de mensajes, moderadores voluntarios con herramientas del bot. Las notas en el suelo (ver [Jefes](../06-contenido/jefes.md)) usan **frases de plantilla** como en Elden Ring, justamente para que no se puedan usar para insultar.
