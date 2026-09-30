# Ronda y acciones

> **Módulo** [04 · Combate](README.md) · **Depende de:** [Clases](../03-personaje/clases-y-especializaciones.md), [Equipamiento](../03-personaje/equipamiento.md) · **Alimenta a:** [Salud](../05-salud/README.md) (por eventos), [Jefes](../06-contenido/jefes.md), [PvP](../06-contenido/pvp.md) · **Estado:** propuesta

**De dónde sale.**
- *World of Warcraft*: trinidad tanque/sanador/daño, amenaza, interrupciones, mecánicas de "agruparse" y "separarse".
- *Elden Ring* y *Dark Souls*: aguante para esquivar y bloquear, y postura que se rompe y abre un golpe crítico.
- *Final Fantasy X*: la cola de turnos siempre visible, y que se puede manipular.
- *Darkest Dungeon*: las filas deciden qué puedes hacer.
- *D&D 5.ª edición*: acción, acción adicional y reacción.
- **TowerWars**: rondas simultáneas de 90 s que ya funcionan en Telegram.

**Por qué este diseño.** En Telegram no hay reflejos: hay lectura y decisión. El combate tiene que premiar **leer bien el aviso y planificar**, que es justamente lo que vuelve difícil a un jefe de Elden Ring cuando se le quita la velocidad.

---

## 1. La ronda

Todo combate se divide en **rondas**. En cada una:

1. **El bot muestra el estado** en un mensaje vivo: vidas, recursos, la cola de iniciativa y **el aviso** de lo que prepara el enemigo.
2. **Todos eligen a la vez**, con temporizador: 45 s en mazmorra, 60-90 s en banda, ninguno en solitario.
3. **Se resuelve en orden de iniciativa** y el mensaje se edita con el resumen.

Elegir a la vez evita esperar uno por uno a otros cuatro jugadores, que en Telegram mata cualquier grupo.

### Qué eliges en cada ronda

| Tipo | Cuántas | Ejemplos |
|---|---|---|
| **Acción** | 1 | Atacar, una habilidad, una técnica de equipo, Meditar, rematar a un derribado |
| **Acción rápida** | 1 (opcional) | Beber una poción, cambiar de fila o de formación, apuntar a una parte, marcar un objetivo, mantener una canción |
| **Reacción preparada** | 1 (opcional, gasta Aguante) | Esquivar, Bloquear, Desviar, Interrumpir |

La reacción se **declara antes** y se dispara solo si pasa lo que esperabas. Si preparaste *Esquivar* y el jefe lanzó el golpe que avisó, lo esquivas; si no pasó nada, gastaste Aguante en vano. Así, leer bien el aviso es la habilidad principal del jugador.

## 2. Las barras

| Barra | Qué es | Cómo se mueve |
|---|---|---|
| ❤️ **Vida** | Lo de siempre | Daño y curación |
| 🔋 **Aguante** (0-5) | La barra de Souls, en fichas | Cada reacción cuesta 1 o 2. Se recupera 1 por ronda, o 2 si no hiciste acción ofensiva. Las armaduras pesadas bajan el máximo |
| 🔷 **Recurso de clase** | Ira, maná, runas… | Según la clase (ver [Clases](../03-personaje/clases-y-especializaciones.md)) |
| 🛡 **Firmeza** | Resistencia al control | Cada aturdimiento, silencio o derribo que recibes la llena. Llena = **inmune al control durante 3 rondas**. Se vacía sola |
| 🟫 **Postura** (solo enemigos grandes) | La postura de Elden Ring y Sekiro | Los golpes pesados, los bloqueos y los desvíos la bajan. Rota = el enemigo queda **aturdido 1 ronda** y la siguiente acción de cada jugador contra él es un **golpe crítico** |

**Firmeza** responde al problema del control encadenado de WoW: nadie puede quedar aturdido más de dos veces seguidas, y funciona igual en PvE y en PvP. En los jefes, es lo que impide encadenarles aturdimientos sin fin.

## 3. Iniciativa

- Cada combatiente tiene **Iniciativa**, que sale de la Celeridad del equipo, del peso de la armadura y de las heridas en las piernas.
- La **cola de las próximas 8 acciones** está siempre a la vista, como en *Final Fantasy X*.
- El Bardo Estratega mueve la cola, ciertos golpes la retrasan y el Clamor la acelera.
- Si hay empate, gana quien eligió primero: así se premia no hacer esperar al grupo.

## 4. Filas y formación

Dos filas por bando:

| Fila | Quién suele estar | Regla |
|---|---|---|
| **Vanguardia** | Tanques, cuerpo a cuerpo | Puede pegar cuerpo a cuerpo y recibe los golpes de frente |
| **Retaguardia** | Distancia, sanadores | No pega cuerpo a cuerpo (salvo lanzas y habilidades de alcance). Mientras haya alguien en vanguardia, los enemigos cuerpo a cuerpo no llegan a ella |

Además, cada jugador tiene una **formación**, que traduce el "agrúpense / sepárense" de las bandas de WoW:

| Formación | Efecto |
|---|---|
| **Agrupado** | Reparte el daño de los golpes "compartidos": cuanta más gente agrupada, menos daño por cabeza. Recibe entero el daño de las explosiones en área |
| **Disperso** | Evita el daño en cadena y en área. Recibe entero el daño compartido, y las curas de área no le llegan |

Los jefes avisan qué viene. "*La bruja marca a tres objetivos con fuego que salta…*": hay que dispersarse. "*El gigante levanta un meteoro sobre el grupo…*": hay que agruparse para repartirlo. Cambiar de fila o de formación es una **acción rápida**.

## 5. Amenaza

- Cada enemigo tiene una tabla de amenaza que el tanque ve: `Coloso → 🎯 Bram (tanque) · 2.º Lyra (+15 %)`.
- **Provocar** obliga al objetivo durante 2 rondas y se reparte entre los tanques del grupo.
- Algunos jefes **no siempre** siguen la amenaza: ciertos movimientos buscan al sanador, al más débil o a quien más daño hizo. El aviso lo dice. En TowerWars, que el jefe busque primero al sanador y después al más débil funcionó bien como presión; aquí es un rasgo de algunos jefes, no de todos.

## 6. Derribado, revivir y huir

- **Derribado.** Al llegar a 0 de vida no mueres: quedas **derribado** 3 rondas, sangrando. Un aliado puede levantarte con una acción; si ya pasó el plazo, hace falta una resurrección en combate. Mientras estás derribado puedes arrastrarte a la retaguardia o usar un objeto de emergencia.
- **Caído.** Si pasan las 3 rondas o recibes un golpe de remate, caes. Qué significa depende de la zona y del modo (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)). Caer siempre deja una herida.
- **Huir.** Es una acción que se resuelve al final de la ronda. Falla si tienes una pierna herida o si te bloquea un enemigo más rápido. A un Guardián no se le huye: se abandona la instancia.

## 7. PvE y PvP no son el mismo combate

| Regla | PvE | PvP |
|---|---|---|
| Firmeza | Sí | Sí, con ventana más larga |
| Amortiguación de curación | No | Sí: desde la ronda 8, −5 % de curación por ronda |
| Tope de golpe | No | Ninguna acción puede quitar más del **40 % de la vida máxima** de un jugador |
| Modificadores por spec | No | Cada spec tiene un ajuste PvP propio (WoW hace lo mismo) |
| Equipo | El tuyo | Normalizado en la arena clasificada (ver [PvP](../06-contenido/pvp.md)) |

## 8. Cómo se ve en Telegram

```
⚔️ Ronda 7 · Guardián del Piso 23 — Coloso de Cristal
Fase 2/3  ❤️ 61% ▓▓▓▓▓▓░░░░   🟫 Postura ▓▓▓▓▓▓▓▓░░

⚠️ El Coloso hunde los puños en el suelo… la tierra
tiembla bajo la VANGUARDIA.

🟥 Tú — Guerrero Protección · Vanguardia · Agrupado
❤️ 842/1.200   💢 Ira 55   🔋 Aguante ●●●○○
🩹 Brazo izq.: corte moderado

Turnos: Tú → Lyra → COLOSO → Bram → Ossian
⏱ 45 s

[🛡 Bloqueo con escudo] [⚔️ Golpe de escudo]
[🗣 Grito desafiante]   [🌀 Torbellino]
[🔁 Fila / Formación]   [🎯 Apuntar]
[🧪 Objetos]            [📜 Registro]
```

Después de resolverse, el mismo mensaje pasa a:

```
Ronda 7 — resumen
🛡 Bloqueaste el Terremoto por la vanguardia (−180 de postura al Coloso)
✨ Lyra cura a Bram 210
💥 Ossian rompe el BRAZO DERECHO del Coloso: pierde "Puño de Cuarzo"
🩸 Bram: contusión en la pierna izquierda (leve)
▸ Registro completo (tocar para abrir)
```

La última línea es una cita plegable con cada número.
