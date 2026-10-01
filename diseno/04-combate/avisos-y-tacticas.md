# Avisos, conocimiento y tácticas automáticas

> **Módulo** [04 · Combate](README.md) · **Depende de:** [Ronda y acciones](ronda-y-acciones.md) · **Alimenta a:** [Jefes](../06-contenido/jefes.md), [Progresión](../03-personaje/progresion.md) (conocimiento), [PvP](../06-contenido/pvp.md) (arena asíncrona) · **Estado:** propuesta, con D-46 (6 botones) aplicada

---

## 1. Avisos: el corazón de la dificultad

**De dónde sale.** Los jefes de WoW anuncian sus golpes ("¡No te quedes en el fuego!"), y los de Elden Ring tienen movimientos reconocibles que se aprenden muriendo. En texto, el aviso es la única ventana que tiene el jugador para leer lo que viene.

Cada movimiento importante de un enemigo grande se **anuncia una ronda antes**, o dos si es devastador, con un texto reconocible:

> ⚠️ *El Coloso hunde los puños en el suelo… la tierra tiembla bajo la **vanguardia**.*

### Cómo se contesta con una sola elección

No hay botón de Defender ni reacción aparte (D-46). Se contesta con lo que llevas en la barra y en el cinturón (ver [Ronda y acciones](ronda-y-acciones.md)):

| Ronda | Qué pasa | Qué puedes hacer |
|---|---|---|
| **La del aviso** | El golpe todavía no cae | Atacar con normalidad, o beber ya una **poción de resistencia** (dura 3 rondas) para tener libre la ronda siguiente |
| **La del golpe** | El golpe cae en el turno del enemigo | Usar tu **respuesta** (bloquear, esquivar, desviar, reposicionarte, proteger) o 🌀 Esquivar donde no se huye. Las respuestas y los objetos se resuelven **antes que cualquier golpe**, así que la iniciativa no importa |

Defenderse cuesta la ronda (esa vez no atacas) y Aguante. Por eso no conviene defenderse de todo: solo de lo que de verdad pega.

| Aviso | Respuesta con habilidad | Respuesta con la Mochila |
|---|---|---|
| Golpe a una fila | 🛡 El tanque bloquea por toda la fila; los demás, 💨 esquivar o 🔁 cambiar de fila | Poción de resistencia del tipo de daño |
| Golpe a un objetivo marcado | Ese jugador usa 💨 o 🤺; un sanador o soporte le pone un 🫧 escudo | Poción de resistencia; poción de vida si ya le pegó |
| Daño en área total | 🫧 Escudos de grupo, defensivas mayores, curas en la ronda siguiente | Poción de resistencia |
| Salto en cadena | 💨 Esquivar o 🔁 reposicionarse: te saca del alcance (dispersarse) | — |
| Golpe compartido | Quedarse para repartirlo; 🛡 bloqueo de fila o 🫧 escudo | Poción de resistencia |
| Canalización | **Interrumpir**: cualquier habilidad con ✋ en esa ronda la corta (si no se interrumpe, el efecto es enorme) | 💣 Bomba de destello |
| Invocación | Cambiar de objetivo a los invocados (elegir objetivo es gratis) | 💣 Bomba en área |
| Estado que se acumula (veneno, fuego) | Habilidades que disipan o limpian | 💊 Remedio de ese estado |

### Los avisos que mienten (a propósito)

Elden Ring es difícil porque sus jefes **retrasan** los golpes. Aquí pasa lo mismo:
- **Retraso.** "*Levanta el hacha… y la sostiene.*" Si usas tu respuesta en esta ronda, gastas la ronda y el Aguante en vano, y el golpe cae en la siguiente: hay que volver a pagar, con menos 🔋. Hay que esperar.
- **Combo.** El mismo aviso anuncia tres golpes en tres rondas. Contestar los tres con respuestas cuesta 3 🔋 y tres rondas sin atacar; una poción de resistencia baja el daño de los tres y solo cuesta una ronda. Quien esquiva el primero y se relaja, cae en el segundo.
- **Finta.** En las fases avanzadas, el jefe amaga y cambia de objetivo. Siempre deja una pista en el texto para quien lee con atención.

### Cómo se ve

Un combo en un Guardián (no se puede huir, así que el quinto botón es 🌀 Esquivar). El jugador gasta esta ronda en la poción de resistencia y ataca libre las tres siguientes.

```
⚔️ Ronda 4 · Guardián de la Hondonada Gris — Reina Ceniza

⚠️ La Reina Ceniza alza las alas: TRES oleadas de fuego
caerán sobre la RETAGUARDIA en las próximas rondas.

🟪 Tú — Mago Fuego ⚔ · Retaguardia
❤️ 590/880   🔷 Maná 410/700   🔋 ●●○○○
🎒 Cinturón: 🧪 Vida ×2 · 🔥 Resist. fuego ×1 · 💊 Ungüento ×1

[⚔️ Atacar]          [✨ Piroexplosión]
[✨ Bola de Fuego]   [💨 Traslación]
[🌀 Esquivar]        [🎒 Mochila]
```

## 2. Conocimiento: aprender a un jefe es progresión

- La primera vez que ves un movimiento, solo tienes el texto.
- Después de verlo 3 veces, el **Bestiario** lo registra y el aviso incluye una pista: *"(Ya conoces este movimiento: golpe retrasado, espera una ronda)"*. También dice su forma (estocada, barrido, aplastamiento…), que indica qué respuesta conviene (ver [Mecánicas avanzadas](mecanicas-avanzadas.md)).
- El Bestiario también guarda debilidades, resistencias y partes rompibles de cada criatura vencida (origen: el bestiario de *Monster Hunter*). Saber qué poción de resistencia llevar es conocimiento puro.
- El conocimiento se puede **comprar y compartir**: el Informante vende fichas de jefes (ver [Profesiones](../07-economia/profesiones.md)), como el informante de SAO que vendía guías de cada piso de su torre.

**Por qué conviene.** Convierte el "aprender el jefe muriendo" de Souls en algo que queda registrado. Además, crea un oficio social: vender información. Y es justo la ventaja que pide D-49: el que sabe más rinde más, con cualquier clase (ver [Balance](../03-personaje/balance.md)).

## 3. Tácticas: el combate cuando no miras

**De dónde sale.** Los *gambits* de *Final Fantasy XII* y las tácticas de *Dragon Age*.

Cada héroe tiene una lista de reglas en orden. Solo pueden usar lo que hay en tu barra de 6 y en tu cinturón:

```
1. Si mi vida < 30 %              → 🎒 Poción de vida
2. Si el aviso es para mí o mi fila → ✨ Evasión
3. Si hay aliado derribado        → 🎒 Levantar
4. Si tengo 5 combos              → ✨ Eviscerar
5. Siempre                        → ⚔️ Atacar
```

**Capa simple y capa profunda (D-44).** Cada rol trae Tácticas por defecto que ya hacen lo básico: contestar los avisos con tu respuesta, beber poción con poca vida, levantar a los caídos y atacar el resto del tiempo. Editarlas, agregar condiciones (apuntar a la cola del jefe mientras esté entera, guardar la poción de resistencia para el combo) es la capa profunda, para quien la busca.

**Dónde se usan:**
- **Cuando se acaba el temporizador** y no elegiste: actúan tus Tácticas en lugar de "no hacer nada".
- **Resolución rápida:** las peleas contra enemigos comunes en misiones, encargos y expediciones se pueden simular enteras, y te llega solo el resultado. Rinde un poco menos que jugar a mano (menos botín, más desgaste), para premiar la atención sin obligarla.
- **Tu Eco:** la copia de tu héroe que otros invocan cuando no estás conectado (ver [Jefes](../06-contenido/jefes.md)) y la que te defiende en la arena asíncrona (ver [PvP](../06-contenido/pvp.md)) pelean con tus Tácticas.

**Dónde no valen:** el asalto al Guardián de una región y la arena clasificada en vivo. Ahí, si se acaba el tiempo, tu héroe usa 🌀 Esquivar si hay un aviso sobre él o su fila, y ⚔️ Atacar si no.

**Por qué conviene.** En Telegram la gente juega entre otras cosas. Las Tácticas hacen que el juego respete su tiempo sin quitarle valor a jugar con atención, y además quitan toda razón para usar un bot pirata (ver [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md)).
